import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_search_finds_user(client, user):
    response = client.get(reverse("search:results"), {"q": user.username})

    assert response.status_code == 200  # noqa: S101
    assert user in response.context["user_results"]  # noqa: S101


@pytest.mark.django_db
def test_search_finds_group(client, group):
    response = client.get(reverse("search:results"), {"q": group.title})

    assert response.status_code == 200  # noqa: S101
    assert group in response.context["group_results"]  # noqa: S101
