from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render
from groups.models import Group


@login_required
def group_chat_room(request, group_id):
    group = Group.objects.get(pk=group_id)
    user_groups = group.members.filter(username=request.user.username)
    if user_groups.count() == 0:
        return HttpResponseForbidden()
    return render(request, "chat/room.html", {"group": group})
