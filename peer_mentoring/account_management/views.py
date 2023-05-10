from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from groups.models import Comment, Post

from .forms import AddFriendForm, AddPhotoForm, CustomUserChangeForm
from .models import FriendRequest, Notification, UserProfile

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


@login_required
def send_friend_request(request, user_id):
    receiver = get_object_or_404(UserProfile, id=user_id)
    if not FriendRequest.objects.filter(
        sender=request.user, receiver=receiver
    ).exists():
        FriendRequest.objects.create(sender=request.user, receiver=receiver)
        Notification.objects.create(
            receiver=receiver,
            text=f"{request.user.username} sent you a friend request.",
        )
    else:
        messages.error(request, "You have already sent a friend request to this user.")
    return redirect("")


def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)
    if friend_request.receiver == request.user:
        request.user.friends.add(
            friend_request.sender
        )  # assumes 'friends' is a ManyToManyField on User
        friend_request.delete()
    return redirect("")


def reject_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)
    if friend_request.receiver == request.user:
        friend_request.delete()
    return redirect("")


def friend_request_index(request):
    friend_requests = FriendRequest.objects.filter(receiver=request.user.userprofile)
    context = {"friend_requests": friend_requests}
    return render(request, "friend_requests_index.html", context)
