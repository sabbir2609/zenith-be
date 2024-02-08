import json
from channels.generic.websocket import AsyncWebsocketConsumer
from iot.tasks import mqtt_client_task, publish_to_mqtt

import logging

logger = logging.getLogger(__name__)


class DeviceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            self.device_id = self.scope["url_route"]["kwargs"]["device_id"]
            self.room_group_name = f"{self.device_id}"

            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()

            self.mqtt_client_task_result = await mqtt_client_task.delay(self.device_id)
        except Exception as e:
            logger.error(f"Failed to connect: {e}")

    async def on_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))

    async def receive(self, text_data):
        data = json.loads(text_data)
        received_data = data["state"]
        logger.info(f"Received data: {received_data}")
        try:
            self.mqtt_client_task_result = await publish_to_mqtt.delay(
                self.device_id, received_data
            )
        except Exception as e:
            logger.error(f"Failed to process received data: {e}")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        print(f"Connection closed for: {self.device_id}")

        if hasattr(self, "mqtt_client_task_result"):
            self.mqtt_client_task_result.revoke(terminate=True)
            logger.info("Disconnected from MQTT Broker!")
