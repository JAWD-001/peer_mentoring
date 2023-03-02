from django.shortcuts import render, redirect

from django.views.generic import CreateView
from django.contrib.auth import authenticate, login, logout
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


def create_user(request):
    form = CreateUserForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'account_management/sign_up', {'form': form})


def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    form = LoginForm(request.POST)
    if form.is_valid():
        user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('home')
    else:
        return 'Login Failed, please check your password or username again'


def logout_view(request):
    logout(request)


