from django.urls import path

from .views import (
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
    path("<int:group_id>/posts/<int:post_id>/", group_show_post, name="show_post"),
]
