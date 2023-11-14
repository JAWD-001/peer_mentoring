from django.contrib import admin

from .models import ChatMessage, PrivateChatMessage


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("user", "group", "message", "added")
    search_fields = ("user", "group", "message")
    list_filter = (
        "group",
        "user",
    )


@admin.register(PrivateChatMessage)
class PrivateChatMessageAdmin(admin.ModelAdmin):
    list_display = ("sender", "receiver", "message", "added")
