from django.urls import path

from . import views

app_name = "chat"

urlpatterns = [
    path("room/<int:group_id>/", views.group_chat_room, name="group_chat_room"),
]
