from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, models
from django.utils.translation import gettext as _

from .models import Photo, UserProfile


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={"placeholder": "Username"})
    )
    password = forms.PasswordInput(attrs={"placeholder": "Password"})

    class Meta:
        model = User
        AuthenticationFormFields = ("username", "password")


class CreateUserForm(UserCreationForm):
    error_messages = {
        "password_mismatch": _("The two password fields didn’t match."),
    }
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]
        error_messages = {
            "username": {
                "unique": "This username is already in use, please choose another.",
                "required": "Username cannot be blank or null",
                "min_length": "Username must be at least 2 characters long",
            },
            "first_name": {
                "required": "First name cannot be blank or null",
                "min_length": "First name must be at least 2 characters long",
            },
            "last_name": {
                "required": "Last name cannot be blank or null",
                "min_length": "Last name must be at least 2 characters long",
            },
            "email": {"required": "Email cannot be null or blank"},
        }
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "First Name"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last Name"}),
            "username": forms.TextInput(attrs={"placeholder": "Username"}),
            "email": forms.TextInput(attrs={"placeholder": "Email"}),
            "password": forms.PasswordInput(
                attrs={"placeholder": "Password from model"}
            ),
        }


class CustomUserChangeForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ["avatar", "title", "bio", "interests"]


class AddPhotoForm(models.ModelForm):
    class Meta:
        model = Photo
        fields = ["image", "description"]


class AddFriendForm(forms.Form):
    user_id = forms.IntegerField(widget=forms.HiddenInput())
