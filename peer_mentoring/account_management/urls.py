from django.urls import path

from .views import home, view_profile

app_name = "account_management"

urlpatterns = [
    path("", home, name="home"),
    path("profile/", view_profile, name="profile_home"),
]
