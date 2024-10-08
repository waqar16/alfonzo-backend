from rest_framework import generics, permissions
from .serializers import LawyerProfileSerializer
from .models import LawyerProfile
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404


# Create a new lawyer profile (if it doesn't exist)
class LawyerProfileCreateView(generics.CreateAPIView):
    serializer_class = LawyerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically associate the authenticated user with the profile
        serializer.save(user=self.request.user)


# Retrieve, update or delete a lawyer profile       
class LawyerProfileDetailUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = LawyerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Check if the user is authenticated
        if not self.request.user.is_authenticated:
            raise PermissionDenied("You must be logged in to access this resource.")

        # Get the LawyerProfile for the authenticated user or raise 404
        return get_object_or_404(LawyerProfile, user=self.request.user)


class LawyerProfileListView(generics.ListAPIView):
    serializer_class = LawyerProfileSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        # Return all lawyer profiles
        return LawyerProfile.objects.all()
