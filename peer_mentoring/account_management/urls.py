from django.urls import path

from .views import home, view_profile

app_name = "account_management"

urlpatterns = [
    path("", home, name="home"),
    path("profile/<int:user_id>", view_profile, name="profile_home"),
]
