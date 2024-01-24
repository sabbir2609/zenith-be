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
