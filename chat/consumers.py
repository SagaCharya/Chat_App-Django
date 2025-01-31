from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Message
from asgiref.sync import sync_to_async
from django.utils import timezone



class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        self.current_user = self.scope['user']
        self.receiver_id = self.scope['url_route']['kwargs']['receiver_id']

        user_ids = sorted([str(self.current_user.id), str(self.receiver_id)])
        self.room_group_name = f"chat_{user_ids[0]}_{user_ids[1]}"

        self.other_user_id = self.receiver_id

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()


    async def disconnect(self, code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print(f"User {self.current_user.id} disconnected")




    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']

            # Save message to database
            new_message = await self.save_message(
                sender_id=self.current_user.id,
                receiver_id=self.receiver_id,
                message=message
            )

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender_id': self.current_user.id,
                    'timestamp': new_message.timestamp.strftime("%H:%M %p"),
                }
            )
        except Exception as e:
            print(f"Error: {e}")
            await self.send(text_data=json.dumps({
                'error': 'Failed to process the message.'
            }))

    @sync_to_async
    def save_message(self, sender_id, receiver_id, message):
        return Message.objects.create(
            sender_id=sender_id,
            receiver_id = receiver_id,
            content = message,
        )

    



    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender_id': event['sender_id'],
            'timestamp': event['timestamp']
        }))
    
    


        