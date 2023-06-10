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
    members = models.ManyToManyField(user)
    moderator = models.ForeignKey(
        user, on_delete=models.CASCADE, related_name="moderator"
    )
    banned_users = models.ManyToManyField(
        User, related_name="banned_from_groups", null=True, blank=True
    )
    # banned = models.ManyToManyField(user)

    def __str__(self):
        return self.title

    def can_join(self, user):
        if user == self.moderator:
            return False
        if user in self.members.all():
            return False
        # if user in self.banned.all():
        #   return False
        # TODO: this could cause n+1 problem
        # https://www.youtube.com/watch?v=e_8JvcP1q48
        if GroupJoinRequest.objects.filter(sender=user, group=self).exists():
            return False
        return True


class GroupJoinRequest(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="group_sent_requests"
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="group_received_requests"
    )
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            "sender",
            "receiver",
        )


class Post(models.Model):
    id = models.BigAutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    content = models.TextField(blank=False, null=True)
    added = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        ordering = ("user__date_joined",)

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

    class Meta:
        ordering = ("user__date_joined",)

    def __str__(self):
        return self.content

    @property
    def is_post_comment(self):
        return self.post

    @is_post_comment.setter
    def post_comment_id(self, new_value: int):
        self.post = new_value
