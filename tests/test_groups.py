import pytest
from django.urls import reverse
from groups.models import Comment, Group, GroupJoinRequest, Post


# from groups.views import group_index, groups_moderated
@pytest.mark.django_db
def test_group_title(group):
    assert group.title == "Test Group"  # noqa: S101


@pytest.mark.django_db
def test_group_can_join(group, user):
    assert not group.can_join(user)  # noqa: S101


@pytest.mark.django_db
def test_group_index_GET(client_authenticated):
    response = client_authenticated.get(reverse("groups:group_home"))
    assert response.status_code == 200  # noqa: S101
    assert "form" in response.context  # noqa: S101
    assert "groups" in response.context  # noqa: S101


@pytest.mark.django_db
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
    group.members.add(user)

    client = client_authenticated
    response = client.get(reverse("groups:groups_joined"))

    assert response.status_code == 200  # noqa: S101
    assert group in response.context["groups"]  # noqa: S101


# tests groups_joined_unauthenticated
@pytest.mark.django_db
def test_groups_joined_unauthenticated(client, user, group):
    group.members.add(user)

    response = client.get(reverse("groups:groups_joined"))
    assert response.status_code == 302  # noqa: S101
    assert "login" in response.url  # noqa: S101


# test groups_moderated view
@pytest.mark.django_db
def test_groups_moderated(client_authenticated, user, group):
    response = client_authenticated.get(reverse("groups:groups_moderated"))

    assert response.status_code == 200  # noqa: S101
    assert group in response.context["groups"]  # noqa: S101
    assert group.title == "Test Group"  # noqa: S101


@pytest.mark.django_db
def test_group_detail_GET(client_authenticated, user, group):
    group.members.add(user)

    response = client_authenticated.get(
        reverse("groups:group_detail", kwargs={"group_id": group.id})
    )

    print(response.content)  # Print the response content

    assert response.status_code == 200  # noqa: S101
    assert user in group.members.all()  # noqa: S101
    assert group.title == "Test Group"  # noqa: S101
    print(response.content)


@pytest.mark.django_db
def test_group_detail_POST(client_authenticated, post):
    post.group.members.add(post.author)

    response = client_authenticated.post(
        reverse("groups:group_detail", kwargs={"group_id": post.group.id}),
        data={"title": post.title, "content": post.content},
    )

    assert response.status_code == 302  # noqa: S101
    assert Post.objects.filter(  # noqa: S101
        group=post.group, content=post.content, title=post.title
    ).exists()


@pytest.mark.django_db
def test_comment_created(comment):
    assert comment.content == "Test"  # noqa: S101


@pytest.mark.django_db
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


@pytest.mark.django_db
def test_send_group_join_request(
    client_authenticated, user, user2, group, join_request
):
    response = client_authenticated.post(
        reverse("groups:send_group_join_request"), data={"group_id": group.id}
    )
    assert response.status_code == 302  # noqa: S101
    assert group.groupjoinrequest_set.filter(sender=user).exists()  # noqa: S101


@pytest.mark.django_db
def test_group_request_index(client_authenticated, group, join_request):
    requests = GroupJoinRequest.objects.filter(group=group)
    response = client_authenticated.get(
        reverse("groups:group_request_index", kwargs={"group_id": group.id})
    )

    assert response.status_code == 200  # noqa: S101
    assert group.id in response.context  # noqa: S101
    assert requests.exists()  # noqa: S101
    assert join_request in response.context["requests"]  # noqa: S101
    assert len(response.context["requests"]) == 1  # noqa: S101


@pytest.mark.django_db
def test_accept_join_request(client_authenticated, group, join_request):
    response = client_authenticated.post(
        reverse(
            "groups:group_approve_join", kwargs={"join_request_id": join_request.id}
        ),
    )

    assert response.status_code == 302  # noqa: S101
    assert response.url == reverse(  # noqa: S101
        "groups:group_request_index", kwargs={"group_id": group.id}
    )
    assert not GroupJoinRequest.objects.filter(  # noqa: S101
        id=join_request.id
    ).exists()  # noqa: S101
    assert f"{join_request.sender.username} has been added to the group."  # noqa: S101


@pytest.mark.django_db
def test_reject_join_request(client_authenticated, user, user2, group, join_request):
    assert GroupJoinRequest.objects.filter(id=join_request.id).exists()  # noqa: S101
    assert group.moderator == user  # noqa: S101

    response = client_authenticated.post(
        reverse(
            "groups:group_reject_request", kwargs={"join_request_id": join_request.id}
        )
    )

    assert not GroupJoinRequest.objects.filter(  # noqa: S101
        id=join_request.id
    ).exists()  # noqa: S101

    assert f"{join_request.sender.username} has been added to the group."  # noqa: S101
    assert response.status_code == 302  # noqa: S101
    assert response.url == reverse(  # noqa: S101
        "groups:group_request_index", kwargs={"group_id": group.id}
    )


@pytest.mark.django_db
def test_delete_post(client_authenticated, user, group):
    post = Post.objects.create(content="Test Content", group=group, author=user)
    response = client_authenticated.post(
        reverse("groups:delete_post", kwargs={"group_id": group.id, "post_id": post.id})
    )
    assert response.status_code == 302  # noqa: S101
    assert not Post.objects.filter(id=post.id).exists()  # noqa: S101


@pytest.mark.django_db
def test_delete_comment(client_authenticated, user, group):
    post = Post.objects.create(content="Test Content", group=group, author=user)
    comment = Comment.objects.create(content="Test Comment", post=post, author=user)
    response = client_authenticated.post(
        reverse(
            "groups:delete_comment",
            kwargs={"group_id": group.id, "post_id": post.id, "comment_id": comment.id},
        )
    )

    assert response.status_code == 302  # noqa: S101
    assert not Comment.objects.filter(id=comment.id).exists()  # noqa: S101


@pytest.mark.django_db
def test_ban_user(client_authenticated, user, user2, group):
    group.moderator = user
    group.save()
    response = client_authenticated.post(
        reverse("groups:ban_user", kwargs={"group_id": group.id, "user_id": user2.id})
    )
    group.refresh_from_db()

    assert response.status_code == 302  # noqa: S101
    assert user2 in group.banned_users.all()  # noqa: S101
    assert f"{user2.username} has been banned."  # noqa: S101
