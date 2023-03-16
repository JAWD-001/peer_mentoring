from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Comments(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=200, blank=False, null=True)
    added = models.DateTimeField(auto_now_add=True, null=False, blank=False)


class Post(models.Model):
    id = models.BigAutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    content = models.TextField(blank=False, null=True)
    comments = models.ManyToManyField(Comments)
    added = models.DateTimeField(auto_now_add=True, null=False, blank=False)
