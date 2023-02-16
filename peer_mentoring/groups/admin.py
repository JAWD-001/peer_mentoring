from django.contrib import admin

from .models import Avatar, Category, Group

# Register your models here.

admin.sites.register(Avatar)
admin.sites.register(Category)
admin.sites.register(Group)