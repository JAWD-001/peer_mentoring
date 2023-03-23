from django.contrib.auth.models import User
from django.db import models
from groups.models import Group

# Create your models here.


class Post(models.Model):
    id = models.BigAutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    content = models.TextField(blank=False, null=True)
    added = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)

    @property
    def is_group_post(self):
        return self.group is not None

    @is_group_post.setter
    def group_post_id(self, new_value: int):
        self.group = new_value


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=200, blank=False, null=True)
    added = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
