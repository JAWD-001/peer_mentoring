from django.db import models

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator

from django.core.validators import MaxLengthValidator, MinLengthValidator, EmailValidator

from django.core.validators import EmailValidator, MinLengthValidator
# Create your models here.

class CustomUser(AbstractUser):
    username_validator = UnicodeUsernameValidator()

    id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=150, blank=False, help_text="Required. 150 characters or less.", validators=[MaxLengthValidator(150), MinLengthValidator(1)], error_messages={'blank':'A first name is required.'})
    last_name = models.CharField(max_length=150, blank=False, help_text="Required. 150 characters or less.", validators=[MaxLengthValidator(150), MinLengthValidator(1)], error_messages={'blank':'A last name is required.'})
    username = models.CharField(max_length=150, unique=True, help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                                validators=[username_validator, MaxLengthValidator(150),MinLengthValidator(1)], error_messages={"unique":"A user with that username already exists."})
    email = models.EmailField(unique=True, blank=False, validators=[EmailValidator()] )
    password = models.CharField(blank=False, max_length=127)