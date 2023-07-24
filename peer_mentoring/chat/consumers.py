import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.id = self.scope["url_route"]["kwargs"]["group_id"]
        self.room_group_name = f"chat_{self.id}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        now = timezone.now()
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "user": self.user.username,
                "datetime": now.isoformat(),
            },
        )
        await self.save_chat_message(message, now)
        self.send(text_data=json.dumps({"message": message}))

    @database_sync_to_async
    def save_chat_message(self, message, now):
        from groups.models import Group  # Moved here

        from .models import ChatMessage  # Moved here

        group = Group.objects.get(id=self.id)
        ChatMessage.objects.create(
            group=group, user=self.user, message=message, added=now.isoformat()
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))


class PrivateChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.sender = self.scope["user"]
        self.receiver_id = self.scope["url_route"]["kwargs"]["receiver_id"]
        ids = sorted([self.sender.id, int(self.receiver_id)])
        self.room_group_name = f"private_chat_{ids[0]}_{ids[1]}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        print(f'Received connect request from {self.scope["user"]}')
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        now = timezone.now()

        if self.scope["user"].id == self.sender.id or self.scope["user"].id == int(
            self.receiver_id
        ):
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message,
                    "user": self.sender.username,
                    "datetime": now.isoformat(),
                },
            )
            await self.save_chat_message(message, now)
            self.send(text_data=json.dumps({"message": message}))

    @database_sync_to_async
    def save_chat_message(self, message, now):
        from django.contrib.auth.models import User  # Moved here

        from .models import PrivateChatMessage  # Moved here

        sender_user = User.objects.get(pk=self.sender.id)
        receiver_user = User.objects.get(pk=int(self.receiver_id))
        PrivateChatMessage.objects.create(
            sender=sender_user,
            receiver=receiver_user,
            message=message,
            added=now.isoformat(),
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))
