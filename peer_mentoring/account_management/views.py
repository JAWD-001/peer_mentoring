from django.shortcuts import render

from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView, PasswordResetConfirmView, LogoutView
from django.urls import reverse_lazy

from .models import CustomUser
from .forms import CreateUserForm, LoginForm, ResetPasswordForm
# Create your views here.


class CreateUserView(CreateView):
    model = CustomUser
    form_class = CreateUserForm
    fields = 'username, first_name, last_name, dob, email '
    template_name = 'account_management/create_user.html'
    success_url = reverse_lazy('account_management:landing')


class UserLoginView(LoginView):
    model = CustomUser
    form_class = LoginForm
    next_page = reverse_lazy('account_management:user_home')

