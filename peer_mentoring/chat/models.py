from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Message(models.Model):
    author = (models.ForeignKey(User, on_delete=models.CASCADE),)
    content = models.TextField()
    added = models.DateTimeField(auto_now_add=True)
