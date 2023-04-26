from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models

user = get_user_model()


class Avatar(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=30, blank=False)
    image = models.ImageField(upload_to="avatar")

    def __str__(self):
        return self.name


class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=30, null=True, blank=False)

    def __str__(self):
        return self.name


class Group(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=50, blank=False, unique=True)
    avatar = models.ForeignKey(Avatar, on_delete=models.CASCADE)
    description = models.TextField(max_length=250, blank=False, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    added = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    moderator = models.ForeignKey(user, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Post(models.Model):
    id = models.BigAutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    content = models.TextField(blank=False, null=True)
    added = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title

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

    def __str__(self):
        return self.content

    @property
    def is_post_comment(self):
        return self.post

    @is_post_comment.setter
    def post_comment_id(self, new_value: int):
        self.post = new_value
