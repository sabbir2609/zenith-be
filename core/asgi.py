import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.security.websocket import AllowedHostsOriginValidator

settings_module = (
    "core.settings.prod" if "WEBSITE_HOSTNAME" in os.environ else "core.settings.dev"
)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)

from core.routing import websocket_urlpatterns  # noqa isort:skip


application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AllowedHostsOriginValidator(URLRouter(websocket_urlpatterns)),
    }
)
