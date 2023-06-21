from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/chat/room/(?P<group_id>\d+)/$", consumers.ChatConsumer.as_asgi()),
    re_path(
        r"ws/chat/private/(?P<receiver_id>\d+)/$",
        consumers.PrivateChatConsumer.as_asgi(),
    ),
]
