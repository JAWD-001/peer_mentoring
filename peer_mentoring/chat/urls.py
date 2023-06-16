from django.urls import path

from . import views

app_name = "chat"

urlpatterns = [
    path("room/<int:group_id>/", views.group_chat_room, name="group_chat_room"),
    # TODO: private chat
    path(
        "room/<int:sender>/<int:receiver>",
        views.private_group_chat_room,
        name="private_chat_room",
    ),
]
