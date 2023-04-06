from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import AddPhotoForm, CreateUserForm, CustomUserChangeForm, LoginForm

# Create your views here.


def home(request):
    return render(request, "account_management/home.html")


@login_required
def view_profile(request):
    user = request.user
    form = CustomUserChangeForm()
    photo_upload = AddPhotoForm()
    if request.method == "POST":
        if form in request.POST:
            if form.is_valid():
                form.save()
                messages.success(request, "Profile Updated!")
        if photo_upload in request.POST:
            if form.is_valid():
                image = form.save(commit=False)
                image.user = request.user
                image.save()
                messages.success(request, "Image Uploaded!")
        else:
            form = CustomUserChangeForm()
            photo_upload = AddPhotoForm()
    context = {
        "user": user,
        "form": form,
        "photo_upload": photo_upload,
    }
    return render(request, "user_profile.html", context)


def create_user(request):
    form = CreateUserForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect("home")
    else:
        form = LoginForm()
    return render(request, "account_management/sign_up", {"form": form})


def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    form = LoginForm(request.POST)
    if form.is_valid():
        user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect("home")
    else:
        return "Login Failed, please check your password or username again"


def logout_view(request):
    logout(request)
