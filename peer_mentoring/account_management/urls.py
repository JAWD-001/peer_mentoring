from django.urls import path

from .views import create_user

app_name = 'account_management'

urlpatterns = [
    path('create/', create_user, name='create_user'),
]