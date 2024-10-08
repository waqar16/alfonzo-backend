from django.urls import path
from .views import NotificationListView, MarkNotificationReadView, DeleteNotificationView


urlpatterns = [
    path('notifications/', NotificationListView.as_view(), name='notification-list'),
    path('notifications/<int:notification_id>/mark-read/', MarkNotificationReadView.as_view(), name='mark-notification-read'),
    path('notifications/<int:notification_id>/delete/', DeleteNotificationView.as_view(), name='delete-notification'),
]
