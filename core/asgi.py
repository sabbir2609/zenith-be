import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

settings_module = (
    "core.settings.prod" if "WEBSITE_HOSTNAME" in os.environ else "core.settings.dev"
)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)

from notification.routing import websocket_urlpatterns  # noqa isort:skip


application = ProtocolTypeRouter(
    {"http": get_asgi_application(), "websocket": URLRouter(websocket_urlpatterns)}
)
