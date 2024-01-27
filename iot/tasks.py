from iot.mqtt.client import client
from celery import shared_task


@shared_task
def run_mqtt_loop():
    client.loop_forever()
