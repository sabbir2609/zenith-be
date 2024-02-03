import json
from channels.generic.websocket import AsyncWebsocketConsumer

from iot.tasks import mqtt_client_task


class DeviceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.device_id = self.scope["url_route"]["kwargs"]["device_id"]
        self.room_group_name = f"{self.device_id}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

        client_id = self.device_id

        self.run_mqtt_task = mqtt_client_task.delay(client_id)

    async def on_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        if hasattr(self, "mqtt_client_task_result"):
            self.mqtt_client_task_result.revoke(terminate=True)
