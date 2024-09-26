from rest_framework import generics, permissions
from .models import Feedback
from .serializers import FeedbackSerializer
from rest_framework.response import Response


class FeedbackListCreateView(generics.ListCreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]  # Restrict access to authenticated users


class FeedbackDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]  # Restrict access to authenticated users


class TopFeedbacksView(generics.ListAPIView):
    queryset = Feedback.objects.all().order_by('-stars')[:5]  # Get top 5 feedbacks
    serializer_class = FeedbackSerializer

    def get(self, request, *args, **kwargs):
        feedbacks = self.get_queryset()
        serializer = self.get_serializer(feedbacks, many=True)
        return Response(serializer.data)
