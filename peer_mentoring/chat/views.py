from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render
from groups.models import Group

from .models import ChatMessage


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
