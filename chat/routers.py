# routers.py
from django.urls import path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    # Using 'path' instead of 're_path'
    path('ws/chat_room/<int:sender_id>/<int:receiver_id>/', ChatConsumer.as_asgi()),
]