from django.contrib import admin
from .models import Interest, Photo, CustomUser, UserProfile

# Register your models here.
admin.site.register(Interest)
admin.site.register(Photo)
admin.site.register(CustomUser)
admin.site.register(UserProfile)