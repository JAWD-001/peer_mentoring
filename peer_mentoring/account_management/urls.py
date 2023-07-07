from django.urls import path

from .views import (
    accept_friend_request,
    friend_request_index,
    home,
    mentor_index,
    profile_home,
    reject_friend_request,
    send_friend_request,
    user_index,
    view_profile,
)

app_name = "account_management"

urlpatterns = [
    path("", home, name="home"),
    path("user_profile/", profile_home, name="profile_home"),
    path("/user_profile/<int:user_id>/", view_profile, name="view_profile"),
    path("user_index/", user_index, name="user_index"),
    path("mentor_index/", mentor_index, name="mentor_index"),
    path("requests/", friend_request_index, name="request_index"),
    path("send_request/user/<int:user_id>/", send_friend_request, name="send_request"),
    path(
        "accept_request/request/<int:request_id>/",
        accept_friend_request,
        name="accept_request",
    ),
    path(
        "reject_request/request/<int:request_id>/",
        reject_friend_request,
        name="reject_request",
    ),
]
