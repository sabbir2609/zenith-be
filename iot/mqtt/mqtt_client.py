import paho.mqtt.client as mqtt
from django.conf import settings
import json


class MQTTClient:
    def __init__(self, broker_address, broker_port, client_id):
        self.client = mqtt.Client(client_id)
        self.client.on_connect = self.on_connect
        self.client.connect(broker_address, broker_port, 60)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

    def publish(self, topic, payload):
        self.client.publish(topic, json.dumps(payload))
