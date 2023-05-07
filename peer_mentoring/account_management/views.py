from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from groups.models import Comment, Post

from .forms import AddFriendForm, AddPhotoForm, CustomUserChangeForm
from .models import UserProfile

# Create your views here.


def home(request):
    return render(request, "account_management/home.html")


@login_required
def profile_home(request):
    user = request.user
    form = CustomUserChangeForm()
    photo_upload = AddPhotoForm()
    # user_photos = Photo.objects.filter(user=user)
    recent_posts = (
        Post.objects.filter(author=request.user).order_by("added").reverse()[0:9]
    )
    recent_comments = (
        Comment.objects.filter(author=request.user).order_by("added").reverse()[0:9]
    )
    if request.method == "POST":
        if request.FILES:
            photo_upload = AddPhotoForm(request.POST, request.FILES)
            if photo_upload.is_valid():
                photo = photo_upload.save(commit=False)
                photo.user = request.user
                photo.save()
                messages.success(request, "Photo Added!")
        else:
            # profile update, the other form on page
            # update is with instance
            form = CustomUserChangeForm(request.POST, instance=request.user.userprofile)
            if form.is_valid():
                form.save()
                messages.success(request, "Profile Updated!")
    else:
        form = CustomUserChangeForm()
        photo_upload = AddPhotoForm()
    context = {
        "user": user,
        "form": form,
        "photo_upload": photo_upload,
        "recent_posts": recent_posts,
        "recent_comments": recent_comments,
    }
    return render(request, "user_profile.html", context)


def view_profile(request, user_id):
    user = get_object_or_404(UserProfile, id=user_id)
    posts = Post.objects.filter(user=user)
    comments = Comment.objects.filter(user=user)

    if request.method == "POST":
        form = AddFriendForm(request.POST)
        if form.is_valid():
            friend = get_object_or_404(UserProfile, id=form.cleaned_data[user_id])
            request.user.friends.add(friend)
            request.user.save()
            return redirect("user_profile", user_id=user_id)
    else:
        form = AddFriendForm(initial={"user_id": user.id})

    context = {
        "user": user,
        "posts": posts,
        "comments": comments,
        "form": form,
    }
    return render(request, "user_profile.html", context)


@login_required
def user_index(request):
    users = UserProfile.objects.all()
    if request.method == "POST":
        if "user_id" in request.POST:
            user_id = request.POST.get("user_id")
            user = get_object_or_404(UserProfile, id=user_id)
            user.friends.add(user_id)
            user.save()
            messages.success(request, "Friend Request Sent")
            return redirect("account_management:view_profile", user_id)
    context = {"users": users}
    return render(request, "profile_index.html", context)
