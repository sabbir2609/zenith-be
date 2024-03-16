import json
from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("notification_group", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("notification_group", self.channel_name)

    async def on_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))


class MessageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        if user.is_anonymous:
            await self.close()
        else:
            await self.channel_layer.group_add(f"user_{user.id}", self.channel_name)
            await self.accept()

    async def disconnect(self, close_code):
        user = self.scope["user"]
        await self.channel_layer.group_discard(f"user_{user.id}", self.channel_name)
        await self.close()

    async def receive(self, text_data):
        user = self.scope["user"]
        data = json.loads(text_data)
        message = data["message"]
        to_user_id = data["to_user_id"]
        await self.create_message(user, to_user_id, message)
