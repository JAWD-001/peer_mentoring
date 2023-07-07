import pytest
from account_management.forms import AddPhotoForm, CustomUserChangeForm
from account_management.models import Photo
from django.contrib.messages import get_messages
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

    with open(photo.image.path, "rb") as img_file:
        Photo.objects.all().delete()

        response = client_authenticated.post(
            reverse("account_management:profile_home"),
            data={"image": img_file, "description": photo.description},
            format="multipart",
        )

    assert response.status_code == 200  # noqa: S101
    assert (  # noqa: S101
        Photo.objects.count() == 1
    ), "Expected one Photo object after the POST request!"

    new_photo = Photo.objects.first()
    assert (  # noqa: S101
        new_photo.description == photo.description
    ), "Description of the newly added photo doesn't match with the provided one!"

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
