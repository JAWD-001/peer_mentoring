from django.urls import path

from .views import home, profile_home, view_profile

app_name = "account_management"

urlpatterns = [
    path("", home, name="home"),
    path("user_profile", profile_home, name="profile_home"),
    path("profile", view_profile, name="view_profile"),
]
