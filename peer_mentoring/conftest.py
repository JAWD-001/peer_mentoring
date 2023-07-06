import io

import pytest
from account_management.models import (
    FriendRequest,
    Interest,
    Notification,
    Photo,
    UserProfile,
)
from django.core.files.base import ContentFile
from django.test import Client
from groups.models import Avatar, Category, Comment, Group, GroupJoinRequest, Post
from PIL import Image
from tests.factories import UserFactory

# from groups.views import group_index, groups_moderated


"""
Fixtures
"""


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


# Creates user instance
@pytest.fixture
def user(db):
    return UserFactory.create()


@pytest.fixture
def user2(db):
    return UserFactory.create()


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
def interest(db):
    return Interest.objects.create(
        name="Interest1",
        image=ContentFile(b"image_content", name="test.png"),
    )


@pytest.fixture
def photo(db, user):
    photo = Photo(name="Test Photo")
    img = Image.new("RGB", (60, 30), color=(73, 109, 137))  # creating a dummy image
    img_file = io.BytesIO()
    img.save(img_file, format="JPEG")
    img_file.name = "test_photo.jpg"
    img_file.seek(0)
    photo.image.save(img_file.name, ContentFile(img_file.read()))
    photo.save()
    return photo
    return Photo.objects.create(
        image=ContentFile(b"image_content", name="test.png"),
        description="A cool photo",
        user=user,
    )


@pytest.fixture
def user_profile(db, user, photo, interest):
    profile = UserProfile.objects.create(
        user=user, avatar=photo, title="Some Title", bio="This is a bio"
    )
    profile.interests.add(interest)
    return profile


@pytest.fixture
def friend_request(db, user_profile):
    # Create another user for the friend request
    user2 = UserFactory.create()
    profile2 = UserProfile.objects.create(user=user2)

    return FriendRequest.objects.create(
        sender=user_profile,
        receiver=profile2,
    )


@pytest.fixture
def notification(db, user_profile):
    return Notification.objects.create(
        receiver=user_profile, text="You have a new notification"
    )
