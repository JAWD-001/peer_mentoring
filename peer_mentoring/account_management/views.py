from django.shortcuts import render

from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView, PasswordResetConfirmView, LogoutView

from .forms import CreateUserForm
# Create your views here.

class CreateUserView(CreateView):
    form_class = CreateUserForm