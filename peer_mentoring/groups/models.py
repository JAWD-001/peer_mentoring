from django.db import models

from peer_mentoring.account_management.models import UserProfile


# Create your models here.

class Avatar(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=30, blank=False)
    image = models.ImageField(upload_to='avatar')

    def __str__(self):
        return self.name


class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=30, blank=False)

    def __str__(self):
        return self.name


class Group(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=50, blank=False, unique=True)
    avatar = models.ForeignKey(Avatar)
    description = models.TextField(max_length=250, blank=False, null=False)
    members = models.ManyToManyField(UserProfile)
    added = models.DateTimeField(auto_now_add=True, null=False, blank=False)

    def __str__(self):
        return self.title
