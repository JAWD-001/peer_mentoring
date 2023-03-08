from django.urls import path

from .views import home, create_user

app_name = 'account_management'

urlpatterns = [
    path('', home)
]