from account_management.models import UserProfile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from .forms import GroupPostCommentForm, GroupPostForm
from .models import Comment, Group, Post

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
    form = GroupPostForm(request.POST)
    context = {
        "group": group,
        "post": post,
        "members": member,
        "form": form,
    }
    if request.metthod == "POST":
        if form.is_valid():
            post = form.save(commit=False)
            post.group = group
            post.author = request.user
            post.save()
            messages.success(request, "Post Added!")
            return render(request, "group_detail.html", context)
        else:
            form = GroupPostForm()
        return render(request, "group_detail.html", {"form": form})


@login_required
def group_show_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    comment = Comment.objects.all(pk=post.id)
    form = GroupPostCommentForm(request.POST)
    context = {
        "post": post,
        "comment": comment,
        "form": form,
    }
    if request.method == "POST":
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            post.author = request.user
            post.save()
            messages.success(request, "Post Added!")
            return render(request, "group_show_post.html", context)
    else:
        form = GroupPostCommentForm()
    return render(request, "group_show_post.html", {"form": form})
