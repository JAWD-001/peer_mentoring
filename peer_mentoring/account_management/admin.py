from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Interest, Photo, CustomUser, UserProfile

# Register your models here.
admin.site.register(Interest)
admin.site.register(Photo)
admin.site.register(CustomUser, UserAdmin)
admin.site.register(UserProfile)

