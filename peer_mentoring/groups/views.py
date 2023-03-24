from account_management.models import UserProfile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import GroupPostCommentForm, GroupPostForm
from .models import Group, Post

# Create your views here.


@login_required
def group_index_view(request):
    groups = Group.objects.all()
    context = {"groups": groups}
    return render(request, "groups_index.html", context)


"""@login_required
def group_posts(request):
    posts = Post.objects.all.filter(id=Group.id)
    comments = request.POST.get(Comment)
    return render(request, "group_detail.html", posts, comments)"""
# commented this out because this is redundant from the context dict
# in group_detail_view


@login_required
def group_members_index_view(request):
    members = UserProfile.objects.all()
    context = {"members": members}
    return render(request, "group_detail.html", context)


# should I just add this to the group_detail_view? thinking that
# I should just add this query into the context dict there


@login_required
def group_detail(request, group_id):
    group = Group.objects.get(pk=group_id)
    posts = Post.objects.filter(group=group)

    if request.method == "POST":
        form = GroupPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.group = group
            post.author = request.user
            post.save()
            messages.success(request, "Post Added!")
            form = GroupPostForm()
    else:
        form = GroupPostForm()

    context = {
        "form": form,
        "posts": posts,
    }
    return render(request, "group_detail.html", context)


@login_required
def show_post(request, post_id):
    pass


@login_required
def group_create_post_comment_view(request, post_id):
    post = Post.objects.get(pk=post_id)
    # TODO: do the same as group_create_post_view
    if request.method == "POST":
        form = GroupPostCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, "Comment added!")
            return redirect("groups:group_detail", comment.id)
    else:
        form = GroupPostCommentForm()
    return render(request, "group_detail.html", {"form": form})
