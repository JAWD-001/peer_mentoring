from django.shortcuts import render
from django.contrib.auth import authenticate, login

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


class UserLoginView(LoginView):
    model = CustomUser
    form_class = LoginForm
    next_page = reverse_lazy()

class ForgotUsernameView(PasswordResetView, SuccessMessageMixin):
    form_class = ForgotUsernameForm
    email_template_name = 'login_app/forgot_username_email.html'
    template_name = 'login_app/forgot_username_form.html'
    success_url = reverse_lazy('login:forgot_username_done')

