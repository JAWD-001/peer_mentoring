from django.urls import path

from .views import create_group_post, group_detail, group_index, group_show_post

app_name = "groups"

urlpatterns = [
    path("", group_index, name="group_home"),
    path("<int:group_id>/", group_detail, name="group_detail"),
    path("<int:group_id>/posts/<int:post_id>/", group_show_post, name="show_post"),
    path("<int:group_id>/create", create_group_post, name="create_post"),
]
