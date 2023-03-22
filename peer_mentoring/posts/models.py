from django.contrib.auth.models import User
from django.db import models
from groups.models import Group

# Create your models here.


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=200, blank=False, null=True)
    added = models.DateTimeField(auto_now_add=True, null=False, blank=False)


class Post(models.Model):
    id = models.BigAutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    content = models.TextField(blank=False, null=True)
    comments = models.ForeignKey(Comment, on_delete=models.CASCADE)
    added = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    is_group_post = models.BooleanField(blank=False, null=False, default=True)
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)
