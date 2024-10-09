from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()

admin.site.register(User)
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'role', 'mfa_enabled']
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('phone', 'role', 'mfa_enabled', 'mfa_method', 'mfa_code', 'totp_secret')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)