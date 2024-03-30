from django.urls import re_path
from .consumers import Consumer

websocket_urlpatterns = [
    re_path("ws/stream", Consumer.as_asgi())
]

