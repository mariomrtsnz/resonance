from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .infrastructure.persistence.models import User, UserProfile

admin.site.register(User, BaseUserAdmin)
admin.site.register(UserProfile) 