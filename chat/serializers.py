from rest_framework import serializers
from main.serializers import UserSerializer
from .models import *


class ChatroomSerializer(serializers.ModelSerializer):
    user1 = UserSerializer(read_only=True)
    user2 = UserSerializer(read_only=True)
    class Meta:
        model = ChatRooms
        fields = ['id', 'user1', 'user2']

class MessageSerializer(serializers.ModelSerializer):

    chat_room = ChatroomSerializer(read_only=True)

    class Meta:
        model = Messages
        fields = ['id', 'chat_room', 'user', 'content', 'timestamp', 'is_read', 'is_send', 'message_type']