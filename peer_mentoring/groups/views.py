from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CreateGroupForm, GroupPostCommentForm, GroupPostForm
from .models import Comment, Group, GroupJoinRequest, Post

# Create your views here.


@login_required
def group_index(request):
    groups = Group.objects.all()
    form = CreateGroupForm()
    if request.method == "POST":
        if "group_id" in request.POST:
            group_id = request.POST.get("group_id")
            group = get_object_or_404(Group, id=group_id)
            group.members.add(request.user)
            group.save()
            messages.success(request, "Joined Group!")
            return redirect("groups:group_detail", group_id)
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            new_group_form = form.save(commit=False)
            new_group_form.moderator = request.user
            new_group_form.save()
            new_group_form.members.add(request.user)
            messages.success(request, "Group Created and User Added as First Member!")
            return redirect("groups:group_home")
    context = {"groups": groups, "form": form}
    return render(request, "groups_index.html", context)


@login_required
def groups_joined(request):
    # groups = Group.objects.filter(member=request.user.userprofile)
    groups = Group.objects.filter(members=request.user)
    context = {
        "groups": groups,
    }
    return render(request, "groups_joined.html", context)


@login_required
def groups_moderated(request):
    # groups = Group.object.filter(moderator=request.user.userprofile)
    groups = Group.objects.filter(moderator=request.user)
    context = {
        "groups": groups,
    }
    return render(request, "groups_moderated.html", context)


@login_required
def group_detail(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    posts = Post.objects.filter(group=group_id)
    # TODO: check if user is member of group to allow access
    # needs to approve
    member = group.members.all()
    if request.user not in member:
        raise PermissionDenied()
    # UserProfile.objects.filter(groups_joined=group_id)
    form = GroupPostForm()
    context = {
        "group": group,
        "posts": posts,
        "members": member,
        "form": form,
    }
    if request.method == "POST":
        form = GroupPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.group = group
            post.author = request.user
            post.save()
            messages.success(request, "Post Added!")
            return redirect("groups:group_detail", group_id)
        else:
            form = GroupPostForm()
    return render(request, "group_detail.html", context)


@login_required
def group_show_post(request, group_id, post_id):
    group = Group.objects.get(id=group_id)
    post = Post.objects.get(id=post_id, group=group)
    comments = Comment.objects.filter(post=post)
    if request.method == "POST":
        form = GroupPostCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, "Comment Added!")
            return redirect("groups:show_post", group_id, post_id)
    else:
        form = GroupPostCommentForm()
    context = {
        "group": group,
        "post": post,
        "comments": comments,
        "form": form,
    }
    return render(request, "groups_show_post.html", context)


@login_required
def send_group_join_request(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if not GroupJoinRequest.objects.filter(user=request.user, group=group).exists():
        GroupJoinRequest.objects.create(user=request.user, group=group)
        messages.success(request, "Group join request sent.")
    else:
        messages.error(request, "You have already sent a join request to this group.")
    return redirect("group_detail", group_id=group_id)


@login_required
def accept_join_request(request, join_request_id):
    join_request = get_object_or_404(GroupJoinRequest, id=join_request_id)
    group = join_request.group
    if group.moderator != request.user:
        raise PermissionDenied()
    group.members.add(join_request.user)
    join_request.delete()
    messages.success(
        request, f"{join_request.user.username} has been added to the group."
    )
    return redirect("manage_group_join_requests", group_id=group.id)


@login_required
def reject_join_request(request, join_request_id):
    join_request = get_object_or_404(GroupJoinRequest, id=join_request_id)
    group = join_request.group
    if group.moderator != request.user:
        raise PermissionDenied()
    join_request.delete()
    messages.success(request, f"{join_request.user.username}'s join request")
