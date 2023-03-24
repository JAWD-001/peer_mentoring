from django.urls import path

from .views import (
    group_create_post_comment_view,
    group_detail,
    group_index_view,
    group_members_index_view,
    show_post,
)

app_name = "groups"

urlpatterns = [
    path("", group_index_view, name="groups_home"),
    path("<int:group_id>", group_detail, name="group_detail"),
    path("posts/<int:post_id>", show_post, name="show_post"),
    path("group_members/", group_members_index_view, name="group_members"),
    path(
        "comments/<int:post_id>",
        group_create_post_comment_view,
        name="group_create_post_comment",
    ),
]
