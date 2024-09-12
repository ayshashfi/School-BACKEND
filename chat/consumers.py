import logging
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from main.models import User
from .models import ChatRooms, Messages

logger = logging.getLogger('chat')

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            self.request_user = self.scope['user']
            if self.request_user.is_authenticated:
                self.chat_with_user = self.scope["url_route"]["kwargs"]["id"]
                user_ids = sorted([int(self.request_user.id), int(self.chat_with_user)])
                self.room_group_name = f"chat_{user_ids[0]}-{user_ids[1]}"
                
                await self.channel_layer.group_add(self.room_group_name, self.channel_name)
                self.chat_room, _ = await self.get_or_create_chat_room()
                await self.accept()
                logger.info(f"WebSocket CONNECT: {self.room_group_name} by user {self.request_user.id}")
            else:
                await self.close()
                logger.warning("WebSocket CLOSE: Unauthorized user")
        except Exception as e:
            logger.error(f"Error in connect: {str(e)}")
            await self.close()

    @database_sync_to_async
    def get_or_create_chat_room(self):
        user1 = self.request_user
        user2 = User.objects.get(id=self.chat_with_user)
        user_ids = sorted([user1.id, user2.id])
        
        chat_room, created = ChatRooms.objects.get_or_create(
            user1_id=user_ids[0],
            user2_id=user_ids[1],
            defaults={'user1_id': user_ids[0], 'user2_id': user_ids[1]}
        )
        return chat_room, created

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            action = data["action"]

            if action == "chat_message":
                message_content = data["message"]
                message_type = data.get("message_type", 'text_message')
                message_id = await self.save_message(message_content, message_type)
                await self.channel_layer.group_send(
                    self.room_group_name, 
                    {
                        "type": "chat_message", 
                        "message_id": message_id,
                        "message": message_content,
                    }
                )
                
            elif action == "read_status_update":
                await self.mark_all_messages_as_read()

        except Exception as e:
            await self.send(text_data=json.dumps({"error": str(e)}))

    @database_sync_to_async
    def save_message(self, message_content, message_type):
        chat_room = self.chat_room
        message = Messages.objects.create(
            chat_room=chat_room,
            user=self.request_user,
            content=message_content,
            message_type=message_type,
        )
        return message.id

    @database_sync_to_async
    def mark_message_as_read(self, message_id):
        try:
            message = Messages.objects.get(id=message_id)
            if message.user.id != self.request_user.id:  # Ensure it's the recipient
                print(message, '..............')
                message.is_read = True
                message.save()
                print(message, '..............')
        except Messages.DoesNotExist:
            pass

    @database_sync_to_async
    def mark_all_messages_as_read(self):
        # Mark all messages in the conversation as read by the current user
        try:
            messages = Messages.objects.filter(chat_room=self.chat_room, is_read=False).exclude(user=self.request_user)
            for message in messages:
                message.is_read = True
                message.save()
        except Exception as e:
            print(f"Error in mark_all_messages_as_read: {str(e)}")

    @database_sync_to_async
    def get_message_object(self, message_id):
        try:
            message = Messages.objects.get(id=message_id)
            message_obj = {
                'id': message.id,
                'chat_room': message.chat_room_id,
                'user': message.user.id,
                'content': message.content,
                'message_type': message.message_type,
                'timestamp': message.timestamp.isoformat(),
                'is_read': message.is_read,
            }
            return message_obj
        except Messages.DoesNotExist:
            return None

    async def chat_message(self, event):
        try:
            message_id = event["message_id"]
            message_obj = await self.get_message_object(message_id)

            # Mark the message as read if the recipient receives it
            if message_obj['user'] != self.request_user.id:  # Recipient received the message
                await self.mark_message_as_read(message_id)
            
            await self.send(text_data=json.dumps(message_obj))
        except Exception as e:
            print(f"Error in chat_message: {str(e)}")

    async def disconnect(self, code):
        try:
            await self.channel_layer.group_discard(
                self.room_group_name, 
                self.channel_name
            )
        except Exception as e:
            print(f"Error in disconnect: {str(e)}")
