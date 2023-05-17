from django.contrib import admin

from .models import (
    Avatar,
    Category,
    Comment,
    Group,
    GroupJoinRequest,
    GroupRequestNotification,
    Post,
)


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
    list_display = ["id", "author", "content", "added", "post"]


@admin.register(GroupJoinRequest)
class GroupRequestAdmin(admin.ModelAdmin):
    list_display = ["id", "sender", "receiver", "created_at"]


@admin.register(GroupRequestNotification)
class GroupRequestNotificationAdmin(admin.ModelAdmin):
    list_display = ["id", "receiver", "text", "created_at"]
