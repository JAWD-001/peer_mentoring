from django.urls import path

from .views import group_detail, group_index, group_show_post

app_name = "groups"

urlpatterns = [
    path("", group_index, name="groups_home"),
    path("<int:group_id>", group_detail, name="group_detail"),
    path("posts/<int:post_id>", group_show_post, name="show_post"),
]
