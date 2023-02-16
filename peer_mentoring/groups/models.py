from django.db import models

from peer_mentoring.account_management.models import UserProfile

from datetime import datetime
# Create your models here.

class Avatar(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=30, blank=False)
    image = models.ImageField(upload_to='avatar')

class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=30, blank=False)

    def __str__(self):
        return self.name


class Group(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=50, blank=False, unique=True)
    avatar = models.ForeignKey(Avatar)
    description = models.TextField(max_length=250, blank=True)
    categories = models.ManyToManyField(Category)
    members = models.ManyToManyField(UserProfile)
    creation_date = models.DateTimeField(default=datetime.now, blank=False)

    def __str__(self):
        return self.title, self.description
