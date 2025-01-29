from channels.generic.websocket import AsyncWebsocketConsumer
import json



class ChatConsumer(AsyncWebsocketConsumer):
    def connect(self):
        pass

    def disconnect(self, code):
        pass


    def receive(self, text_data):
        pass

    def send_message(self, message):
        pass