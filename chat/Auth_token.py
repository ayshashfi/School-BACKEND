import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from channels.db import database_sync_to_async
from main.models import User


class JwtAuthentication(BaseAuthentication):

    @database_sync_to_async
    def authenticate_websocket(self, scope, token):
        try:
            # Decode the JWT token
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']
            
            # Retrieve the user based on the user_id
            user = User.objects.get(id=user_id)
            # print("auth_token_user_id: ", user_id)
            
            return user
        
        except User.DoesNotExist:
            raise AuthenticationFailed('Unauthenticated')
        
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')