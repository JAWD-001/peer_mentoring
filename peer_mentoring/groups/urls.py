from django.urls import path

from .views import (
    ban_user,
    delete_comment,
    delete_post,
    group_detail,
    group_index,
    group_show_post,
    groups_joined,
    groups_moderated,
    send_group_join_request,
)

app_name = "groups"

urlpatterns = [
    path("", group_index, name="group_home"),
    path(
        "groups_join_request/", send_group_join_request, name="send_group_join_request"
    ),
    path("groups_joined/", groups_joined, name="groups_joined"),
    path("groups_moderated/", groups_moderated, name="groups_moderated"),
    path("<int:group_id>/", group_detail, name="group_detail"),
    path(
        "group/<int:group_id>/posts/<int:post_id>/", group_show_post, name="show_post"
    ),
    path("group/<int:group_id>/ban_user/<int:user_id>/", ban_user, name="ban_user"),
    path(
        "group/<int:group_id>/delete_post/<int:post_id/>",
        delete_post,
        name="delete_post",
    ),
    path(
        "group/<int:group_id>/post/<int:post_id>/delete_comment/<int:comment_id>/",
        delete_comment,
        name="delete_comment",
    ),
]
