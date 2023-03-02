from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Interest, Photo, UserProfile

# Register your models here.
@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image')


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'description', 'user')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'avatar', 'title', 'bio')




