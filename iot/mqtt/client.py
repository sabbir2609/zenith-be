from django.conf import settings
import paho.mqtt.client as mqtt


def on_connect(mqtt_client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully " + str(rc))
        mqtt_client.subscribe("ac/temperature")
    else:
        print("Bad connection. Code:", rc)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    message = msg.topic + " " + str(msg.payload)

    from asgiref.sync import async_to_sync
    from channels.layers import get_channel_layer

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "AC118",
        {
            "type": "on_message",
            "message": message,
        },
    )


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(
    host=settings.MQTT_HOST,
    port=settings.MQTT_PORT,
    keepalive=settings.MQTT_KEEPALIVE,
)
