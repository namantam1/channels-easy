from django.urls import re_path

from .consumers import NewConsumer

websocket_urlpatterns = [
    re_path(r"ws/test/$", NewConsumer.as_asgi()),
]
