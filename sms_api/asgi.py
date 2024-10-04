import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application

# Set the Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sms_api.settings")

# Setup Django
django.setup()

# Get the default Django ASGI application
django_asgi_app = get_asgi_application()

from chat.routing import websocket_urlpatterns
from chat.channels_middleware import JWTwebsocketMiddleware

# Define the application with ProtocolTypeRouter
application = ProtocolTypeRouter({
    "http": django_asgi_app,  
    "websocket": JWTwebsocketMiddleware(
        AuthMiddlewareStack(
            URLRouter(
                websocket_urlpatterns
            )
        )
    ),
})