from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Message
from asgiref.sync import sync_to_async
from django.utils import timezone



class ChatConsumer(AsyncWebsocketConsumer):
    active_connections = {} 
    async def connect(self):
        self.room_group_name = self.scope['url_route']['kwargs']['room_name']
        self.current_user = self.scope['user']


        parts = self.room_group_name.split('_')
        if len(parts) == 3:
            try:
                user_id1 = int(parts[1])
                user_id2 = int(parts[2])
            except ValueError:
            
                await self.close()
                return

            
            if self.current_user.id == user_id1:
                self.receiver_id = user_id2
            elif self.current_user.id == user_id2:
                self.receiver_id = user_id1
            else:
                
                await self.close()
                return
        else:
    
            await self.close()
            return
        
        if self.room_group_name not in self.active_connections:
            self.active_connections[self.room_group_name] = set()
        self.active_connections[self.room_group_name].add(self.channel_name)

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()


    async def disconnect(self, code):

        if self.room_group_name in self.active_connections:
            self.active_connections[self.room_group_name].discard(self.channel_name)
            if not self.active_connections[self.room_group_name]:
                del self.active_connections[self.room_group_name]  
        
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print(f"User {self.current_user.id} disconnected")




    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json.get('message')
            file_url = text_data_json.get('file_url')
            if message and len(message) > 1000:
                raise ValueError("Message is too long")
        
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
            'error': 'Invalid JSON format.'
            }))
            return 
        except ValueError as e:
            await self.send(text_data=json.dumps({'error': str(e)}))
            return
        except Exception as e:
            print(f"Error: {e}")
            await self.send(text_data=json.dumps({
                    'error': 'Failed to process the message.'
                }))
            return

        new_message = await self.save_message(
        sender_id=self.current_user.id,
        receiver_id=self.receiver_id,
        message=message,
        file_url=file_url  # if you extend your save_message to accept this
    )


        await self.channel_layer.group_send(
            self.room_group_name,
            {
            'type': 'chat_message',
            'message': message,
            'sender_id': self.current_user.id,
            'timestamp': new_message.timestamp.strftime("%H:%M %p"),
            'file_url': file_url,
            'file_name': file_url.split('/')[-1] if file_url else None
        }
        )


    @sync_to_async
    def save_message(self, sender_id, receiver_id, message, file_url=None):
        print(f"Sending to to: {len(self.active_connections[self.room_group_name])} connections")  # Debugging
        new_message = Message.objects.create(
            sender_id=sender_id,
            receiver_id = receiver_id,
            content = message if message else '',
            file = file_url,
        )
    
        return new_message



    async def chat_message(self, event):
        file_url = event.get('file_url')
        file_name = event.get('file_name', 'File')  
        file_type = None

        if file_url:
            if file_url.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                file_type = 'image'
            elif file_url.lower().endswith('.pdf'):
                file_type = 'pdf'
            elif file_url.lower().endswith(('.doc', '.docx')):
                file_type = 'word'
            else:
                file_type = 'other'

        print(f"Sending message: {event['message']} from {event['sender_id']}")
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender_id': event['sender_id'],
            'timestamp': event['timestamp'],
            'file_url': event.get('file_url', None),
            'file_name': file_name,
            'file_type': file_type 
        }))
    
    


        