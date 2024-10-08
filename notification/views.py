from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer


class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return only notifications for the logged-in user
        return Notification.objects.filter(user=self.request.user)


class MarkNotificationReadView(generics.UpdateAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'notification_id'

    def update(self, request, *args, **kwargs):
        try:
            notification = Notification.objects.get(id=kwargs['notification_id'], user=request.user)
            notification.is_read = True
            notification.save()
            return Response({'status': 'Notification marked as read'}, status=status.HTTP_200_OK)
        except Notification.DoesNotExist:
            return Response({'error': 'Notification not found'}, status=status.HTTP_404_NOT_FOUND)


class DeleteNotificationView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'notification_id'

    def delete(self, request, *args, **kwargs):
        try:
            notification = Notification.objects.get(id=kwargs['notification_id'], user=request.user)
            notification.delete()
            return Response({'status': 'Notification deleted'}, status=status.HTTP_200_OK)
        except Notification.DoesNotExist:
            return Response({'error': 'Notification not found'}, status=status.HTTP_404_NOT_FOUND)
