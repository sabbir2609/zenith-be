from django.urls import path
from notification.channels.consumers import NotificationConsumer
from iot.channels.consumers import IotConsumer


websocket_urlpatterns = [
    path("ws/notifications/", NotificationConsumer.as_asgi()),
    path("ws/iot/", IotConsumer.as_asgi()),
]
