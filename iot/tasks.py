# iot/task.py

from celery import shared_task
import paho.mqtt.client as mqtt
from asgiref import sync
from channels.layers import get_channel_layer
from django.conf import settings

from django.core.exceptions import ObjectDoesNotExist


@shared_task(bind=True)
def mqtt_client_task(device_client_id):
    from iot.models import Device

    try:
        device = Device.objects.get(client_id=device_client_id)
        topic = device.topic
        print(topic)
    except ObjectDoesNotExist as e:
        return

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!", rc)
        else:
            print("Failed to connect, return code %d\n", rc)
        client.subscribe(f"{topic}")

    def on_message(client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))
        channel_layer = get_channel_layer()
        sync.async_to_sync(channel_layer.group_send)(
            f"{device.id}", {"type": "device.message", "message": msg.payload.decode()}
        )

    client = mqtt.Client()

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(settings.MQTT_HOST, settings.MQTT_PORT, settings.MQTT_KEEPALIVE)
    client.loop_forever()
