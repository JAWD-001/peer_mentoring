import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # maybe this needs to be pulling from the userprofile?
        self.user = self.scope["user"]
        # same thing but for groups?
        self.id = self.scope["url_route"]["kwargs"]["group_id"]
        # should the room group name be the same as groups.id?
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
        self.send(text_data=json.dumps({"message": message}))

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))
