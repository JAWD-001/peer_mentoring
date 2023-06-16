from django.contrib.auth.models import User
from django.db import models


class ChatMessage(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(max_length=300, blank=False, null=False)
    added = models.DateTimeField(auto_now_add=True, null=False, blank=False)
