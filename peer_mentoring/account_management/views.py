from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from groups.models import Comment, Post

from .forms import AddPhotoForm, CustomUserChangeForm
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
    recent_posts = Post.objects.filter(author=user).order_by("added")[0:10]
    recent_comments = Comment.objects.filter(author=user).order_by("added")[0:10]
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


@login_required
def view_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    posts = Post.objects.filter(author=user)
    comments = Comment.objects.filter(author=user)
    context = {
        "user": user,
        "posts": posts,
        "comments": comments,
    }
    return render(request, "other_user_profile.html", context)


@login_required
def user_index(request):
    profiles = UserProfile.objects.all().exclude(user=request.user)
    context = {"profiles": profiles}
    return render(request, "profile_index.html", context)


@login_required
def mentor_index(request):
    mentors = request.user.userprofile.friends.all()
    context = {
        "mentors": mentors,
    }
    return render(request, "mentor_index.html", context)


@login_required
def send_friend_request(request, user_id):
    receiver = get_object_or_404(User, id=user_id)
    if not FriendRequest.objects.filter(
        sender=request.user.userprofile, receiver=receiver.userprofile
    ).exists():
        FriendRequest.objects.create(
            sender=request.user.userprofile, receiver=receiver.userprofile
        )
        Notification.objects.create(
            receiver=receiver.userprofile,
            text=f"{request.user.username} sent you a friend request.",
        )
        # TODO
        messages.success(request, "Friend Request sent!")
    else:
        messages.error(request, "You have already sent a friend request to this user.")
    return redirect("account_management:view_profile", user_id)


def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)
    if friend_request.receiver == request.user.userprofile:
        friend_request.receiver.friends.add(
            friend_request.sender
        )  # assumes 'friends' is a ManyToManyField on User
        friend_request.sender.friends.add(
            friend_request.receiver
        )  # assumes 'friends' is a ManyToManyField on User

        friend_request.accepted = True
        friend_request.save()

        # TODO
        messages.success(request, "success message")
    return redirect("account_management:request_index")


def reject_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)
    if friend_request.receiver == request.user.userprofile:
        friend_request.delete()
        # TODO
        messages.success(request, "Friend request rejected")
    return redirect("account_management:request_index")


def friend_request_index(request):
    friend_requests = FriendRequest.objects.filter(
        receiver=request.user.userprofile
    ).filter(accepted=False)
    context = {"friend_requests": friend_requests}
    return render(request, "friend_requests_index.html", context)
