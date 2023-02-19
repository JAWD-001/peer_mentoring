from .models import CustomUser, UserProfile

from django import forms
from django.forms import ModelForm, models

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, PasswordResetForm
from django.contrib.auth import password_validation

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder':'Username'}))
    password = forms.PasswordInput(attrs={'placeholder':'Password'})

    class Meta:
        model = CustomUser
        AuthenticationFormFields = ('username', 'password')

class CreateUserForm(UserCreationForm):
    class UserCreationForm(forms.ModelForm):
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
            model = CustomUser
            fields = ("username",)
            error_messages = {
                'username':{
                    'unique':'This username is already in use, please choose another.'
                }
            }
