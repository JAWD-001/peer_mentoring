from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from peer_mentoring.account_management.models import UserProfile

from .models import Group

# Create your views here.


@login_required
def group_index_view(request):
    groups = Group.objects.all()
    context = {"groups": groups}
    return render(request, "groups_index.html", context)


@login_required
def group_view(request, detail_id):
    group = get_object_or_404(Group, pk=detail_id)
    context = {
        "group": group,
    }
    return render(request, "group_detail.html", context)


@login_required
def group_members_index_view(request):
    members = UserProfile.objects.all()
    context = {"members": members}
    return render(request, "group_member_index", context)
