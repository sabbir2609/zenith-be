import json
from channels.generic.websocket import AsyncWebsocketConsumer


class IotConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("iot_group", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("iot_group", self.channel_name)

    async def send_notification(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))
