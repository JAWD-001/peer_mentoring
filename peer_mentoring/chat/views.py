from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.shortcuts import render
from groups.models import Group

from .models import ChatMessage, PrivateChatMessage


@login_required
def group_chat_room(request, group_id):
    group = Group.objects.get(pk=group_id)
    chat_messages = ChatMessage.objects.filter(group=group)

    user_groups = group.members.filter(username=request.user.username)
    if user_groups.count() == 0:
        return HttpResponseForbidden()

    context = {
        "group": group,
        "chat_messages": chat_messages,
    }
    return render(request, "chat/room.html", context)


@login_required
def private_chat_room(request, sender_id, receiver_id):
    sender = User.objects.get(pk=sender_id)
    receiver = User.objects.get(id=receiver_id)

    private_chat_messages = PrivateChatMessage.objects.filter(
        sender=sender, receiver=receiver
    )

    private_group = sender.userprofile.friends.filter(user=receiver)
    if private_group.count() == 0:
        return HttpResponseForbidden()

    context = {
        "receiver": receiver,
        "receiver_id": receiver_id,
        "private_group": private_group,
        "private_chat_messages": private_chat_messages,
    }
    return render(request, "chat/private_chatroom.html", context)
