from django.db import models
from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator

from django.core.validators import MaxLengthValidator, MinLengthValidator, EmailValidator

from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Interest(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=30, blank=True, null=True, unique=True)
    image = models.FileField(blank=True, null=True, unique=True, upload_to="interests")

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    username_validator = UnicodeUsernameValidator()

    id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=150, blank=False, help_text="Required. 150 characters or less.", validators=[MaxLengthValidator(150), MinLengthValidator(1)], error_messages={'blank':'A first name is required.'})
    last_name = models.CharField(max_length=150, blank=False, help_text="Required. 150 characters or less.", validators=[MaxLengthValidator(150), MinLengthValidator(1)], error_messages={'blank':'A last name is required.'})
    dob = models.DateField(blank=False, help_text="Required, please enter a date", )
    username = models.CharField(max_length=150, blank=False, unique=True, help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                                validators=[username_validator, MaxLengthValidator(150),MinLengthValidator(1)], error_messages={"unique":"A user with that username already exists."})
    email = models.EmailField(unique=True, blank=False, validators=[EmailValidator()] )
    password = models.CharField(blank=False, max_length=127)
    date_joined = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.first_name, self.last_name, self.dob, self.username, self.email, self.date_joined


class Photo(models.Model):
    id = models.BigAutoField(primary_key=True)
    image = models.ImageField(blank=False, upload_to='photos')
    description = models.CharField(blank=True, max_length=200)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE())

    def __str__(self):
        return self.description


class UserProfile(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    avatar = models.ForeignKey(Photo, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True)
    interests = models.ManyToManyField(Interest, blank=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    @receiver(post_save, sender=CustomUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=CustomUser)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
