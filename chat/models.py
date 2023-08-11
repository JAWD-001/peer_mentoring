from django.contrib.auth.models import User
from django.db import models
from groups.models import Group


class ChatMessage(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(max_length=300)
    added = models.DateTimeField(auto_now_add=True)


class PrivateChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="receiver"
    )
    message = models.TextField(max_length=300)
    added = models.DateTimeField(auto_now_add=True)
