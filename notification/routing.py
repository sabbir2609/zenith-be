from django.urls import path
from notification.consumers import NotificationConsumer


websocket_urlpatterns = [
    path("ws/notifications/", NotificationConsumer.as_asgi()),
]
