from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render


# Create your views here.
@login_required
def group_chat_room(request, group_id):
    try:
        group = request.user.userprofile.groups_joined.get(id=group_id)
    except:
        return HttpResponseForbidden()
    return render(request, "chat/room.html", {"group": group})
