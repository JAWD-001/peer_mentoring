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
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Group Added!")
            return redirect("groups:group_home")
    context = {"groups": groups, "form": form}
    return render(request, "groups_index.html", context)


"""
@login_required
def groups_joined(request):
    groups = request.user.groups_joined
    context = {
        "groups": groups,
    }
    if request.method == "GET":
        if request.user in groups:
            return render(request, "groups_joined.html", context)
        else:
            return redirect(request, "groups:group_home")
"""


@login_required
def join_group(request, group_id):
    group = Group.objects.get(pk=group_id)
    user = UserProfile.objects.get(request.user)
    context = {
        "group": group,
        "user": user,
    }
    if request.method == "POST":
        user.groups_joined.add(group_id)
        user.save()
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
    member = UserProfile.objects.all()
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
            return redirect("groups:group_detail", group_id, context)
        else:
            form = GroupPostForm()
    return render(request, "group_detail.html", context)


@login_required
def group_show_post(request, group_id, post_id):
    post = Post.objects.get(id=group_id)
    comment = Comment.objects.filter(pk=post_id)
    form = GroupPostCommentForm()
    context = {
        "post": post,
        "comment": comment,
        "form": form,
    }
    if request.method == "POST":
        form = GroupPostCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, "Comment Added!")
            return render(request, "groups_show_post.html", context)
    else:
        form = GroupPostCommentForm()
    return render(request, "groups_show_post.html", {"form": form})
