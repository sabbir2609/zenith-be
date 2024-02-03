from celery import shared_task
from paho.mqtt import client as mqtt_client_module
from asgiref import sync
from channels.layers import get_channel_layer
from django.conf import settings


@shared_task
def mqtt_client_task(device_client_id):
    from iot.models import Device

    device = Device.objects.get(client_id=device_client_id)
    topic = device.topic

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

        client.subscribe(topic)

    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        channel_layer = get_channel_layer()
        sync.async_to_sync(channel_layer.group_send)(
            f"{device.id}", {"type": "device.message", "message": msg.payload.decode()}
        )

    mqtt_client_instance = mqtt_client_module.Client(device_client_id)
    mqtt_client_instance.on_connect = on_connect
    mqtt_client_instance.on_message = on_message
    mqtt_client_instance.connect(
        settings.MQTT_HOST, settings.MQTT_PORT, settings.MQTT_KEEPALIVE
    )
    mqtt_client_instance.loop_start()
