from django.contrib import admin
from .models import UserProfile, UserDocument, UserDevice

# Admin for UserProfile model
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'email', 'phone', 'membership', 'theme', 'notifications', 'prefered_language']
    search_fields = ['user__username', 'first_name', 'last_name', 'email', 'phone']
    list_filter = ['membership', 'theme', 'notifications', 'prefered_language']
    ordering = ['user__username']

# Admin for UserDocument model
@admin.register(UserDocument)
class UserDocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'selected_lawyer', 'created_at', 'updated_at']
    search_fields = ['title', 'user__user__username', 'selected_lawyer__user__username']
    list_filter = ['created_at', 'updated_at']
    ordering = ['created_at']

# Admin for UserDevice model
@admin.register(UserDevice)
class UserDeviceAdmin(admin.ModelAdmin):
    list_display = ['user', 'device_identifier', 'last_login']
    search_fields = ['user__username', 'device_identifier']
    list_filter = ['last_login']
    ordering = ['last_login']