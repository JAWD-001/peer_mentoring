from django.urls import path

from . import views


urlpatterns = [
    path('room/<int:group_id>/', views.group_chat_room, name='group_chat_room'),

]