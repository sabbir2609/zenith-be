import json
from channels.generic.websocket import AsyncWebsocketConsumer
from iot.tasks import run_mqtt_loop


class DeviceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.device_id = self.scope["url_route"]["kwargs"]["device_id"]
        self.room_group_name = f"{self.device_id}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

        self.run_mqtt_loop_result = run_mqtt_loop.delay()

    async def on_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        if hasattr(self, "run_mqtt_loop_result"):
            self.run_mqtt_loop_result.revoke(terminate=True)
