from account_management.models import UserProfile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import GroupPostCommentForm, GroupPostForm
from .models import Group, Post

# Create your views here.


@login_required
def group_index(request):
    groups = Group.objects.all()
    context = {"groups": groups}
    return render(request, "groups_index.html", context)


@login_required
def group_detail(request, pk):
    group = get_object_or_404(Group, pk=pk)
    post = Post.objects.all(pk=group.id)
    member = UserProfile.objects.all()
    context = {
        "group": group,
        "post": post,
        "members": member,
    }
    if request.metthod == "POST":
        form = GroupPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.group = group
            post.author = request.user
            post.save()
            messages.success(request, "Post Added!")
            form = GroupPostForm()
            return render(request, "group_detail.html", context)
        else:
            form = GroupPostForm()
        return render(request, "group_detail.html", {"form": form})


@login_required
def group_show_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    if request.method == "POST":
        form = GroupPostCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            post.author = request.user
            post.save()
            messages.success(request, "Post Added!")
            comment = GroupPostCommentForm()
            return redirect("groups:show_post", post.id)
    else:
        form = GroupPostCommentForm()
    return render(request, "group_detail.html", {"form": form})
