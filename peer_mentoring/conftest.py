import io
from io import BytesIO

import pytest
from account_management.models import (
    FriendRequest,
    Interest,
    Notification,
    Photo,
    UserProfile,
)
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.files.images import ImageFile
from django.test import Client
from groups.models import Avatar, Category, Comment, Group, GroupJoinRequest, Post
from PIL import Image
from tests.factories import UserFactory

# from groups.views import group_index, groups_moderated


"""
Fixtures
"""


@pytest.fixture
def user(db):
    return UserFactory.create()


@pytest.fixture
def user2(db):
    return UserFactory.create()


@pytest.fixture
def interest(db):
    return Interest.objects.create(
        name="Interest1",
        image=ContentFile(b"image_content", name="test.png"),
    )


# Fixture creates an avatar instance for group fixture
@pytest.fixture
def avatar(db):
    avatar = Avatar(name="Test Avatar")
    img = Image.new("RGB", (60, 30), color=(73, 109, 137))  # creating a dummy image
    img_file = io.BytesIO()
    img.save(img_file, format="JPEG")
    img_file.name = "test_image.jpg"
    img_file.seek(0)
    avatar.image.save(img_file.name, ContentFile(img_file.read()))
    avatar.save()
    return avatar


# Fixture creates a category instance for group
@pytest.fixture
def category(db):
    return Category.objects.create(name="Test Category")


# fixture handles client authentication
@pytest.fixture
def client_authenticated(user):
    client = Client()
    client.login(username=user.username, password="12345")  # noqa: S106
    return client


@pytest.fixture
def client2_authenticated(user2):
    client = Client()
    client.login(username=user2.username, password="12345")  # noqa: S106
    return client


# Fixture creates a group instance
@pytest.fixture
def group(db, avatar, category, user):
    group = Group.objects.create(
        title="Test Group",
        avatar=avatar,
        description="This is a test group",
        category=category,
        moderator=user,
    )
    group.members.add(user)
    return group


@pytest.fixture
def join_request(db, user, user2, group):
    return GroupJoinRequest.objects.create(
        sender=user, receiver=group.moderator, group=group
    )


# Fixture to make post instance
@pytest.fixture
def post(db, user, group):
    return Post.objects.create(
        author=user, title="Test Post Title", content="Test Post Content", group=group
    )


@pytest.fixture
def comment(db, user, post):
    return Comment.objects.create(
        author=user,
        content="Test",
        post=post,
    )


@pytest.fixture
def photo(db, user):
    # create an in-memory image file with Pillow
    image_file = BytesIO()
    Image.new("RGB", (100, 100)).save(image_file, "JPEG")
    image_file.seek(0)

    photo = Photo.objects.create(
        image=ImageFile(image_file, name="test.jpg"),
        description="A cool photo",
        user=user,
    )
    return photo


@pytest.fixture
def user_profile(db, user, photo, interest):
    user_profile = UserProfile.objects.get(user=user)
    user_profile.avatar = photo
    user_profile.title = "Some Title"
    user_profile.bio = "This is a bio"
    user_profile.interests.add(interest)
    user_profile.save()
    return user_profile


@pytest.fixture
def user_profile2(db, user2, photo, interest):
    user_profile2 = UserProfile.objects.get(user=user2)
    user_profile2.avatar = photo
    user_profile2.title = "Some Title"
    user_profile2.bio = "This is a bio"
    user_profile2.interests.add(interest)
    user_profile2.save()
    return user_profile


@pytest.fixture
def friend_request(db, user_profile):
    sender = User.objects.create(username="sender", password="123")  # noqa: S106
    sender_profile = sender.userprofile
    sender_profile.title = "Some Other Title"
    sender_profile.save()
    receiver = user_profile
    friend_request = FriendRequest.objects.create(
        sender=sender_profile, receiver=receiver
    )

    return friend_request


@pytest.fixture
def notification(db, user_profile):
    return Notification.objects.create(
        receiver=user_profile, text="You have a new notification"
    )
