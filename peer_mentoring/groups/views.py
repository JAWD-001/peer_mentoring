from account_management.models import UserProfile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CreateGroupForm, GroupPostCommentForm, GroupPostForm
from .models import Comment, Group, Post

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
            messages.success(request, "Group Added!")
            return redirect("groups:group_home")
    context = {"groups": groups, "form": form}
    return render(request, "groups_index.html", context)


@login_required
def groups_joined(request):
    # groups = Group.objects.filter(member=request.user.userprofile)
    groups = request.user.userprofile.groups_joined.all()
    context = {
        "groups": groups,
    }
    return render(request, "groups_joined.html", context)


@login_required
def groups_moderated(request):
    # groups = Group.object.filter(moderator=request.user.userprofile)
    groups = request.user.userprofile.groups_moderated.all()
    context = {
        "groups": groups,
    }
    return render(request, "groups_moderated.html", context)


@login_required
def join_group(request, group_id):
    group = Group.objects.get(pk=group_id)
    userprofile = request.user.userprofile
    context = {
        "group": group,
    }
    if request.method == "POST":
        userprofile.groups_joined.add(group_id)
        return redirect("groups:group_detail", group_id)
    else:
        return render(request, "group_detail.html", context)


@login_required
def leave_group(request, group_id):
    group = Group.objects.get(pk=group_id)
    user = UserProfile.objects.get(request.user)
    context = {
        "group": group,
        "user": user,
    }
    if request.method == "POST":
        if group in user.groups_joined:
            user.groups_joined.remove(group_id)
            return redirect("groups:group_home")
        else:
            return render(request, context)


@login_required
def group_detail(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    posts = Post.objects.filter(group=group_id)
    member = group.members.all()
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
    else:
        form = GroupPostCommentForm()
    context = {
        "group": group,
        "post": post,
        "comments": comments,
        "form": form,
    }
    return render(request, "groups_show_post.html", context)
