from django.shortcuts import render
from rest_framework import generics, status
from .serializers import MessageSerializer, ChatroomSerializer
from .models import ChatRooms, Messages
from django.db.models import Q
from rest_framework.exceptions import NotFound
from rest_framework.response import Response 
from rest_framework.decorators import api_view
from django.db.models import Count

class MessageListView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        user_id1 = self.kwargs['user_id1']
        user_id2 = self.kwargs['user_id2']

        try:
            chat_room = ChatRooms.objects.filter(
                Q(user1_id=user_id1, user2_id=user_id2) | Q(user1_id=user_id2, user2_id=user_id1)
            ).first()  # Get the first matching chat room

            if not chat_room:
                raise NotFound('Room not found')

            # Retrieve the last 20 messages, ordered by timestamp
            messages = Messages.objects.filter(chat_room=chat_room).order_by('-timestamp')[:20]
            return messages
        except ChatRooms.DoesNotExist:
            return Messages.objects.none()


@api_view(['POST'])
def AddChatRoom(request):
    if request.method == 'POST':
        try:
            user_id1 = request.data.get('user_id1')
            user_id2 = request.data.get('user_id2')

            # Ensure user_id1 and user_id2 are different
            if user_id1 == user_id2:
                return Response({'error': 'Cannot create chat room with the same user.'}, status=status.HTTP_400_BAD_REQUEST)

            # Query for existing chat rooms
            chat_rooms = ChatRooms.objects.filter(
                Q(user1_id=user_id1, user2_id=user_id2) | Q(user1_id=user_id2, user2_id=user_id1)
            )

            # Check if chat room already exists
            if chat_rooms.exists():
                chat_room = chat_rooms.first()  # Get the first found chat room
                serializer = ChatroomSerializer(chat_room)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                # Create a new chat room if none exists
                chat_room = ChatRooms.objects.create(user1_id=user_id1, user2_id=user_id2)
                serializer = ChatroomSerializer(chat_room)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def AddMessage(request):
    if request.method == 'POST':
        try:
            chat_room_id = request.data.get('chat_room_id')
            content = request.data.get('content')
            user = request.user  # Assuming you have user authentication set up

            # Create a new message
            message = Messages.objects.create(chat_room_id=chat_room_id, user=user, content=content)

            # Limit messages to the last 30
            messages = Messages.objects.filter(chat_room_id=chat_room_id).order_by('timestamp')

            # Check if the count exceeds 30
            if messages.count() > 30:
                # Delete all messages except the last 30
                messages[:-30].delete()

            print(f"Current message count: {messages.count()}")

            return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['GET'])    
def ListChatUsers(request, user_id):
    if request.method == 'GET':
        try:
            users = ChatRooms.objects.filter(Q(user1_id=user_id) | Q(user2_id=user_id))
            if not users:
                return Response({'message': 'No chat rooms found '})
            serializer = ChatroomSerializer(users, many=True)
            return Response(serializer.data)

        except ChatRooms.DoesNotExist:
            return ChatRooms.objects.none()

class ChatNotificationView(generics.ListAPIView):
    serializer_class = ChatroomSerializer

    def get_queryset(self):
        user = self.request.user
        chat_rooms = ChatRooms.objects.filter(Q(user1=user) | Q(user2=user))
        
        # Annotate each chat room with the count of unread messages
        chat_rooms = chat_rooms.annotate(
            unread_messages_count=Count(
                'message',
                filter=Q(message__is_read=False) & ~Q(message__user=user)
            )
        )
        
        notifications = [
            {'chat_room_id': chat_room.id, 'unread_messages_count': chat_room.unread_messages_count}
            for chat_room in chat_rooms
        ]
        return notifications

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        return Response(queryset)
