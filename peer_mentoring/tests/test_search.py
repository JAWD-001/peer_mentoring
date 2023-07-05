import io

import pytest
from django.core.files.base import ContentFile
from django.urls import reverse
from factories import UserFactory
from groups.models import Avatar, Category, Group
from PIL import Image


@pytest.fixture
def user(db):
    return UserFactory()


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


def test_search_finds_user(client, user):
    response = client.get(reverse("search:results"), {"q": user.username})

    assert response.status_code == 200  # noqa: S101
    assert user in response.context["user_results"]  # noqa: S101


def test_search_finds_group(client, group):
    response = client.get(reverse("search:results"), {"q": group.title})

    assert response.status_code == 200  # noqa: S101
    assert group in response.context["group_results"]  # noqa: S101
