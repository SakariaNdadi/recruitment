import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
import apps.notifications.routing as notifications

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rms.settings.base')

django_asgi_app = get_asgi_application()

application =ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(URLRouter(notifications.websocket_urlpatterns))
    ),
})