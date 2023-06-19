import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from django.utils import timezone
from groups.models import Group

from .models import ChatMessage, PrivateChatMessage


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
        # sort the ids to create a unique room name for the chat between these two users
        ids = sorted([self.sender.id, int(self.receiver_id)])
        self.room_group_name = f"private_chat_{ids[0]}_{ids[1]}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        now = timezone.now()

        # only allow messages from the two users in the chat
        if self.sender.id == int(self.receiver_id) or self.sender.id == int(
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
        sender = User.objects.get(id=self.sender_id)
        PrivateChatMessage.objects.create(
            reciever=self.receiver_id,
            sender=sender,
            message=message,
            added=now.isoformat(),
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))
