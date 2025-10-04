import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import productions.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'filmhub.settings')

# Get the default HTTP application
http_application = get_asgi_application()

# Define the WebSocket application
application = ProtocolTypeRouter({
    "http": http_application,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            productions.routing.websocket_urlpatterns
        )
    ),
})