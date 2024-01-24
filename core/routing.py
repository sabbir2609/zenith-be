from django.urls import path, re_path
from notification.channels.consumers import NotificationConsumer
from iot.channels.consumers import DeviceConsumer


websocket_urlpatterns = [
    path("ws/notifications/", NotificationConsumer.as_asgi()),
    re_path(r"^ws/device/(?P<device_id>\w+)/$", DeviceConsumer.as_asgi()),
]
