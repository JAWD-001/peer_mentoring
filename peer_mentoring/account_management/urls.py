from django.urls import path

from .views import home, profile_home, user_index, view_profile

app_name = "account_management"

urlpatterns = [
    path("", home, name="home"),
    path("user_profile/", profile_home, name="profile_home"),
    path("<int:user_id>/", view_profile, name="view_profile"),
    path("user_index/", user_index, name="user_index"),
]
