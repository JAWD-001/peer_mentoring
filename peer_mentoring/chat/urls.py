from django.urls import path

from . import views

app_name = "chat"

urlpatterns = [
    path("room/group/<int:group_id>/", views.group_chat_room, name="group_chat_room"),
    # TODO: private chat
    path(
        "room/sender/<int:sender>/receiver/<int:receiver>",
        views.private_chat_room,
        name="private_chat_room",
    ),
]
