# iot/task.py

import json
from celery import shared_task
import paho.mqtt.client as mqtt
from asgiref import sync
from channels.layers import get_channel_layer
from django.conf import settings
import paho.mqtt.publish as publish

import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True)
def mqtt_client_task(self, device_client_id):
    from iot.models import Device

    device = Device.objects.get(client_id=device_client_id)
    topic = device.topic

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            logger.info("Connected to MQTT Broker! RC: %d", rc)
        else:
            logger.error("Failed to connect, return code %d", rc)
        client.subscribe(f"{topic}")

    def on_disconnect(client, userdata, rc):
        logger.info("Disconnected from MQTT Broker! RC: %d", rc)

    def on_message(client, userdata, msg):
        logger.info("Received message: %s", msg.payload.decode())

        channel_layer = get_channel_layer()
        sync.async_to_sync(channel_layer.group_send)(
            f"{device_client_id}",
            {"type": "on_message", "message": msg.payload.decode()},
        )

    client = mqtt.Client()

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    client.connect(settings.MQTT_HOST, settings.MQTT_PORT, settings.MQTT_KEEPALIVE)
    client.loop_forever()


@shared_task(bind=True)
def publish_to_mqtt(self, device_client_id, received_data):
    from iot.models import Device

    device = Device.objects.get(client_id=device_client_id)
    topic = device.topic

    mqtt_message = json.dumps({"message": received_data})

    try:
        publish.single(
            topic,
            payload=mqtt_message,
            hostname=settings.MQTT_HOST,
            port=settings.MQTT_PORT,
        )
        logger.info("Published to MQTT: Topic='%s', Message='%s'", topic, mqtt_message)
    except Exception as e:
        logger.error(f"Error publishing to MQTT: {e}")
