from django.urls import path

from .views import (
    group_create_post_comment_view,
    group_create_post_view,
    group_detail_view,
    group_index_view,
    group_members_index_view,
)

app_name = "groups"

urlpatterns = [
    path("", group_index_view, name="groups_home"),
    path("group_detail/<int:pk>", group_detail_view, name="group_detail"),
    path("group_members/", group_members_index_view, name="group_members"),
    path(
        "create_post/<int:group_id>",
        group_create_post_view,
        name="group_create_post_view",
    ),
    path(
        "comments/<int:post_id>",
        group_create_post_comment_view,
        name="group_create_post_comment",
    ),
]
