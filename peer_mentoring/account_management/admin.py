from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Interest, Photo, CustomUser, UserProfile

# Register your models here.
@admin.register
class InterestAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image')


@admin.register
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image', 'description', 'user')


@admin.register
class CustomUser(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'dob', 'username'
                    'email', 'password', 'date_joined')

class UserProfile(admin.ModelAdmin):
    list_display = ('id', 'user', 'avatar', 'title', 'bio', 'interests')




