from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'message', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at', 'user')  # Filters by 'is_read' status, 'created_at' date, and user
    search_fields = ('message', 'user__username')  # Allows searching by message or user's username
    actions = ['mark_as_read']  # Adds a custom action to mark notifications as read

    # Define the custom action to mark notifications as read
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)

    # Short description for the action
    mark_as_read.short_description = 'Mark selected notifications as read'

    # Optionally, you can add more filters or refine existing ones:
    date_hierarchy = 'created_at'  # Adds a date hierarchy for filtering by creation date
    ordering = ('-created_at',)  # Orders the notifications by most recent by default