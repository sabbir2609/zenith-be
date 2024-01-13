from django.urls import path
from notification.consumers import NotificationConsumer


websocket_urlpatterns = [
    path("ws/notification/", NotificationConsumer.as_asgi()),
]
