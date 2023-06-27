import io

import pytest
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.test import Client
from django.urls import reverse
from groups.models import Avatar, Category, Comment, Group, Post
from PIL import Image

# from groups.views import group_index, groups_moderated


"""Fixtures"""


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


# Fixture creates a category instance
@pytest.fixture
def category(db):
    return Category.objects.create(name="Test Category")


# Fixture creates a user instance
@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", password="12345")  # noqa: S106


# fixture handles client authentication
@pytest.fixture
def client_authenticated(user):
    client = Client()
    client.login(username="testuser", password="12345")  # noqa: S106
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


"""View Tests"""


def test_group_title(group):
    assert group.title == "Test Group"  # noqa: S101


def test_group_can_join(group, user):
    assert not group.can_join(user)  # noqa: S101


def test_group_index_GET(client_authenticated):
    response = client_authenticated.get(reverse("groups:group_home"))
    assert response.status_code == 200  # noqa: S101
    assert "form" in response.context  # noqa: S101
    assert "groups" in response.context  # noqa: S101


def test_group_index_POST(client_authenticated, user, avatar, category):
    new_group = {
        "title": "Test Group",
        "avatar": avatar.id,  # use a valid id for fk  noqa: S101
        "description": "Test Description",
        "category": category.id,  # use a valid id for fk  noqa: S101
    }
    response = client_authenticated.post(reverse("groups:group_home"), data=new_group)
    assert response.status_code == 302  # Check redirect  # noqa: S101
    assert Group.objects.filter(  # noqa: S101
        title="Test Group"
    ).exists()  # Check if the group was created


@pytest.mark.django_db
def test_groups_joined_authenticated(client_authenticated, user, group):
    # Add the user to the group's members
    group.members.add(user)

    # Log in the user
    client = client_authenticated

    # Send a GET request to the view
    response = client.get(reverse("groups:groups_joined"))

    # Assert the response status code is 200 (OK)
    assert response.status_code == 200  # noqa: S101

    # Assert the user's group is in the response context
    assert group in response.context["groups"]  # noqa: S101


# tests groups_joined_unauthenticated
@pytest.mark.django_db
def test_groups_joined_unauthenticated(client, user, group):
    # Add the user to the group's members
    group.members.add(user)

    # Send a GET request to the view without logging in
    response = client.get(reverse("groups:groups_joined"))

    # Assert the response status code is 302 (redirect)
    assert response.status_code == 302  # noqa: S101

    # Assert the user is being redirected to the login page
    assert "login" in response.url  # noqa: S101


# test groups_moderated view
@pytest.mark.django_db
def test_groups_moderated(client_authenticated, user, group):
    # Send a GET request to the view
    response = client_authenticated.get(reverse("groups:groups_moderated"))

    # Assert the response status code is 200 (OK)
    assert response.status_code == 200  # noqa: S101

    # Assert the user's group is in the response context
    assert group in response.context["groups"]  # noqa: S101

    # Assert the response contains the title of the group
    assert group.title in str(response.content)  # noqa: S101


def test_group_detail_GET(client_authenticated, user, group):
    # Add the user to the group's members

    group.members.add(user)

    # Send a GET request to the view
    response = client_authenticated.get(
        reverse("groups:group_detail", kwargs={"group_id": group.id})
    )

    # Assert the response status code is 200 (OK)
    assert response.status_code == 200  # noqa: S101

    # Assert that user in group members
    assert user in group.members.all()  # noqa: S101

    # Assert the response contains the title of the group
    assert group.title in str(response.content)  # noqa: S101


@pytest.mark.django_db
def test_group_detail_POST(client_authenticated, post):
    # Add the user to the post's group members
    post.group.members.add(post.author)

    # Send a POST request to the view
    response = client_authenticated.post(
        reverse("groups:group_detail", kwargs={"group_id": post.group.id}),
        data={"title": post.title, "content": post.content},
    )

    # Assert the response status code is 302 (Redirection)
    assert response.status_code == 302  # noqa: S101

    # Assert a new post has been added to the group
    assert Post.objects.filter(  # noqa: S101
        group=post.group, content=post.content, title=post.title
    ).exists()


@pytest.mark.django_db
def test_comment_created(comment):
    assert comment.content == "Test"  # noqa: S101


def test_group_show_post_GET(client_authenticated, user, group, post, comment):
    url = reverse("groups:show_post", kwargs={"group_id": group.id, "post_id": post.id})
    response = client_authenticated.get(url)
    assert response.status_code == 200  # noqa: S101
    assert post == response.context["post"]  # noqa: S101
    assert comment in response.context["comments"]  # noqa: S101


@pytest.mark.django_db
def test_group_show_post_POST(client_authenticated, user, group, post):
    url = reverse("groups:show_post", kwargs={"group_id": group.id, "post_id": post.id})
    comment_data = {"content": "Test comment."}
    response = client_authenticated.post(url, comment_data)
    assert response.status_code == 302  # noqa: S101
    assert Comment.objects.filter(  # noqa: S101
        content="Test comment.", author=user, post=post
    ).exists()
