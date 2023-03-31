from django.forms import ModelForm

from .models import Category, Comment, Group, Post


class CreateGroupCategory(ModelForm):
    model = Category
    fields = ["name"]


class CreateGroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ["title", "avatar", "description", "category"]


class GroupPostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]


class GroupPostCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
