import io

import pytest
from account_management.forms import AddPhotoForm, CustomUserChangeForm
from account_management.models import FriendRequest, Photo
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.core.files import File
from django.core.files.storage import default_storage
from django.http import request
from django.urls import reverse


@pytest.mark.django_db
def test_profile_home_get(client_authenticated, user):
    response = client_authenticated.get(reverse("account_management:profile_home"))
    assert response.status_code == 200  # noqa: S101
    assert isinstance(response.context["form"], CustomUserChangeForm)  # noqa: S101
    assert isinstance(response.context["photo_upload"], AddPhotoForm)  # noqa: S101
    assert response.context["user"] == user  # noqa: S101


@pytest.mark.django_db
def test_profile_home_post_photo(client_authenticated, user, photo):
    assert (  # noqa: S101
        photo.description is not None
    ), "Photo instance doesn't have a description!"  # noqa: S101

    # Fetch the photo file from S3 using Django's default storage (which should be set to S3 in your settings)
    photo_file_content = default_storage.open(photo.image.name).read()

    # Convert the content to an in-memory file (BytesIO) for the test client post request
    img_file = io.BytesIO(photo_file_content)
    img_file.name = photo.image.name

    Photo.objects.all().delete()

    response = client_authenticated.post(
        reverse("account_management:profile_home"),
        data={"image": File(img_file), "description": photo.description},
        format="multipart",
    )

    assert response.status_code == 200  # noqa: S101
    assert (  # noqa: S101
        Photo.objects.count() == 1
    ), "Expected one Photo object after the POST request!"  # noqa: S101

    new_photo = Photo.objects.first()
    assert (  # noqa: S101
        new_photo.description == photo.description
    ), "Description of the newly added photo doesn't match with the provided one!"  # noqa: S101

    assert "Photo Added!" in list(  # noqa: S101
        map(str, list(get_messages(response.wsgi_request)))
    )


@pytest.mark.django_db
def test_profile_home_post_update_profile(client_authenticated, user_profile):
    form_data = {
        "title": "Some Title",
        "bio": "This is a bio",
    }
    response = client_authenticated.post(
        reverse("account_management:profile_home"), data=form_data
    )
    user_profile.refresh_from_db()
    assert response.status_code == 200  # noqa: S101
    assert user_profile.title == "Some Title"  # noqa: S101
    assert user_profile.bio == "This is a bio"  # noqa: S101


@pytest.mark.django_db
def test_view_profile(client_authenticated, user_profile, user):
    response = client_authenticated.get(
        reverse("account_management:view_profile", kwargs={"user_id": user.id})
    )

    assert response.status_code == 200  # noqa: S101
    assert "user" in response.context  # noqa: S101
    assert response.context["user"] == user  # noqa: S101


@pytest.mark.django_db
def test_user_index(client_authenticated, user_profile):
    response = client_authenticated.get(reverse("account_management:user_index"))

    assert response.status_code == 200  # noqa: S101
    assert "profiles" in response.context  # noqa: S101
    for profile in response.context["profiles"]:
        assert profile != request.user  # noqa: S101


@pytest.mark.django_db
def test_mentor_index(client_authenticated, user_profile, user):
    response = client_authenticated.get(reverse("account_management:mentor_index"))

    assert response.status_code == 200  # noqa: S101
    assert "mentors" in response.context  # noqa: S101
    for mentor in response.context["mentors"]:
        assert mentor != request.user  # noqa: S101


@pytest.mark.django_db
def test_send_friend_request(client_authenticated, user_profile, user):
    response = client_authenticated.post(
        reverse("account_management:send_request", kwargs={"user_id": user.id})
    )

    assert response.status_code == 302  # noqa: S101
    assert response.url == reverse(  # noqa: S101
        "account_management:view_profile", kwargs={"user_id": user.id}
    )


@pytest.mark.django_db
def test_accept_friend_request(
    client_authenticated, user_profile, user, friend_request
):
    client_authenticated.force_login(user)

    sender = friend_request.sender
    receiver = friend_request.receiver
    assert sender not in receiver.friends.all()  # noqa: S101
    assert receiver not in sender.friends.all()  # noqa: S101

    assert not friend_request.accepted  # noqa: S101

    response = client_authenticated.post(
        reverse("account_management:accept_request", args=[friend_request.id])
    )

    assert response.status_code == 302  # noqa: S101

    friend_request.refresh_from_db()

    if not friend_request.accepted:
        print("Friend Request not accepted")

    assert friend_request.accepted  # noqa: S101


@pytest.mark.django_db
def test_reject_friend_request(client_authenticated, user_profile, friend_request):
    client_authenticated.force_login(user_profile.user)

    assert not friend_request.accepted  # noqa: S101

    assert FriendRequest.objects.filter(id=friend_request.id).exists()  # noqa: S101

    response = client_authenticated.post(
        reverse("account_management:reject_request", args=[friend_request.id])
    )

    assert not FriendRequest.objects.filter(id=friend_request.id).exists()  # noqa: S101

    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 1  # noqa: S101
    assert str(messages[0]) == "Friend request rejected"  # noqa: S101

    assert response.status_code == 302  # noqa: S101
    assert response.url == reverse("account_management:request_index")  # noqa: S101


@pytest.mark.django_db
def test_friend_request_index(client_authenticated, user_profile, friend_request):
    client_authenticated.force_login(user_profile.user)

    sender2 = User.objects.create(username="sender2", password="123")  # noqa: S106
    sender2_profile = sender2.userprofile
    sender2_profile.title = "Some Other Title"
    sender2_profile.save()
    friend_request2 = FriendRequest.objects.create(
        sender=sender2_profile, receiver=user_profile
    )

    response = client_authenticated.get(reverse("account_management:request_index"))

    assert response.status_code == 200  # noqa: S101

    friend_requests = response.context["friend_requests"]
    assert len(friend_requests) == 2  # noqa: S101
    assert friend_request in friend_requests  # noqa: S101
    assert friend_request2 in friend_requests  # noqa: S101
