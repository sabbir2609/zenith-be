from iot.mqtt.client import client
from celery import shared_task


@shared_task
def run_mqtt():
    client.loop_forever()
