from django.db import models

from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator, MinLengthValidator, EmailValidator
from groups.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Interest(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=30, blank=False, unique=True)
    image = models.FileField(blank=True, null=True, unique=True, upload_to="interests")

    def __str__(self):
        return self.name


class Photo(models.Model):
    id = models.BigAutoField(primary_key=True)
    image = models.ImageField(blank=False, upload_to='photos')
    description = models.CharField(blank=True, null=True, max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.description


class UserProfile(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ForeignKey(Photo, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=150, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    interests = models.ManyToManyField(Interest)
    dob = models.DateField(blank=True, null=True, help_text="Required, please enter a date", )
    groups_joined = models.ManyToManyField(Group)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
