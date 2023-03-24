from django.forms import ModelForm

from .models import Comment, Post


class GroupPostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]


class GroupPostCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
