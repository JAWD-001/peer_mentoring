from django.db import models
from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator

from django.core.validators import MaxLengthValidator, MinLengthValidator, EmailValidator

from django.core.validators import EmailValidator, MinLengthValidator
# Create your models here.
class Interest(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=30, blank=True, unique=True)
    image = models.FileField(blank=True, null=True, unique=True, upload_to="interests")

    def __str__(self):
        return self.name

class Photo(models.Model):
    id = models.BigAutoField(primary_key=True)
    image = models.ImageField(blank=False, upload_to='photos')
    description = models.CharField(blank=True, max_length=200)

    def __str__(self):
        return self.description

class CustomUser(AbstractUser):
    username_validator = UnicodeUsernameValidator()

    id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=150, blank=False, help_text="Required. 150 characters or less.", validators=[MaxLengthValidator(150), MinLengthValidator(1)], error_messages={'blank':'A first name is required.'})
    last_name = models.CharField(max_length=150, blank=False, help_text="Required. 150 characters or less.", validators=[MaxLengthValidator(150), MinLengthValidator(1)], error_messages={'blank':'A last name is required.'})
    username = models.CharField(max_length=150, unique=True, help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                                validators=[username_validator, MaxLengthValidator(150),MinLengthValidator(1)], error_messages={"unique":"A user with that username already exists."})
    email = models.EmailField(unique=True, blank=False, validators=[EmailValidator()] )
    password = models.CharField(blank=False, max_length=127)
    date_joined = models.DateTimeField(default=datetime.now)

class UserProfile(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    avatar = models.ForeignKey(Photo, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    interests = models.ManyToManyField(Interest, blank=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
