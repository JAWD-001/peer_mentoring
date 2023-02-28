from django.urls import path

from .views import CreateUserView, LoginView

app_name = 'account_management'

urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create'),
    path('', LoginView.as_view(), name='landing'),
]