from django.urls import path

from peer_mentoring.groups.views import (
    group_index_view,
    group_members_index_view,
    group_view,
)

app_name = "groups"

urlpatterns = [
    path("", group_index_view, name="groups_home"),
    path("group_detail/<int:pk>", group_view, name="group_detail"),
    path("group_members/", group_members_index_view, name="group_members"),
]
