import io

import pytest
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from groups.models import Avatar, Category, Group
from PIL import Image

User = get_user_model()

# from groups.views import groups_moderated


@pytest.mark.django_db
def test_groups_moderated_view():
    pass


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


@pytest.fixture
def category(db):
    return Category.objects.create(name="Test Category")


@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", password="12345")  # noqa: S106


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


def test_group_title(group):
    assert group.title == "Test Group"  # noqa: S101


def test_group_can_join(group, user):
    assert not group.can_join(user)  # noqa: S101
