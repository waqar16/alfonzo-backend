from django.urls import path
from .views import NotificationListView, MarkNotificationReadView, DeleteNotificationView, MarkAllNotificationsReadView


urlpatterns = [
    path('notifications/', NotificationListView.as_view(), name='notification-list'),
    path('notifications/<int:notification_id>/mark-read/', MarkNotificationReadView.as_view(), name='mark-notification-read'),
    path('notifications/<int:notification_id>/delete/', DeleteNotificationView.as_view(), name='delete-notification'),
    path('notifications/<int:notification_id>/mark-all-read/', MarkAllNotificationsReadView.as_view(), name='delete-all-notifications'),
]
