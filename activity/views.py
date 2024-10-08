from rest_framework import generics, permissions
from .models import Activity
from .serializers import ActivitySerializer


class ActivityListCreateView(generics.ListCreateAPIView):
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Optionally restricts the returned activities to a given user,
        by filtering against a `user` query parameter in the URL.
        """
        queryset = Activity.objects.all().order_by('-timestamp')
        user_id = self.request.query_params.get('user', None)
        if user_id is not None:
            queryset = queryset.filter(user__id=user_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ActivityRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Ensure that users can only access their own activities.
        """
        return Activity.objects.filter(user=self.request.user)
