from django.contrib import admin

from .models import Avatar, Category, Comment, Group, Post


@admin.register(Avatar)
class AvatarAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "image")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "avatar", "description", "added")


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "title", "content", "added", "group")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["author", "content", "added", "post"]
