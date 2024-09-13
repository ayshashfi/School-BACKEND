import os
import django
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sms_api.settings')

# Initialize Django application
django.setup()  # Call setup before importing anything else Django-related

# Now import other necessary modules
from chat.routing import websocket_urlpatterns
from chat.channels_middleware import JWTwebsocketMiddleware

# Initialize Django ASGI application
django_asgi_app = get_asgi_application()

# Define the ASGI application protocol types
application = ProtocolTypeRouter({
    'http': django_asgi_app,  # HTTP protocol using Django ASGI app
    'websocket': AllowedHostsOriginValidator(  # WebSocket protocol with allowed hosts validation
        JWTwebsocketMiddleware(  # Custom JWT middleware for WebSocket
            AuthMiddlewareStack(  # Authentication middleware for WebSocket
                URLRouter(websocket_urlpatterns)  # URL routing for WebSocket
            )
        )
    ),
})

