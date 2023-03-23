from account_management.models import UserProfile
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from posts.models import Comment, Post

from .forms import GroupPostCommentForm, GroupPostForm
from .models import Group

# Create your views here.


@login_required
def group_index_view(request):
    groups = Group.objects.all()
    context = {"groups": groups}
    return render(request, "groups_index.html", context)


@login_required
def group_detail_view(request):
    group = get_object_or_404(Group, pk=Group.id)
    context = {
        "group": group,
    }
    return render(request, "group_detail.html", context)


@login_required
def group_posts(request):
    posts = Post.objects.all.filter(id=Group.id)
    comments = request.POST.get(Comment)
    return render(request, "group_detail.html", posts, comments)


@login_required
def group_members_index_view(request):
    members = UserProfile.objects.all()
    context = {"members": members}
    return render(request, "group_detail.html", context)


@login_required
def group_create_post_view(request):
    if request.method == "POST":
        form = GroupPostForm(request.POST)
        if form.is_valid():
            post = form.save()
            return redirect("group-detail", post.id)
    else:
        form = GroupPostForm()
    return render(request, "group_detail.html", {"form": form})


@login_required
def group_create_post_comment_view(request):
    if request.method == "POST":
        form = GroupPostCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = group_posts
            comment.save()
            return redirect("group-detail", comment.id)
    else:
        form = GroupPostForm()
    return render(request, "group_detail.html", {"form": form})
