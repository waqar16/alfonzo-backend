from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


User = get_user_model()


class UserAdmin(BaseUserAdmin):
    def save_model(self, request, obj, form, change):
        if not change:  # This means the user is being created
            obj.set_password(obj.password)  # Hash the password
        super().save_model(request, obj, form, change)


admin.site.register(User, UserAdmin)
