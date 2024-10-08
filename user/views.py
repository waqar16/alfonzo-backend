from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from .models import UserProfile, UserDocument
from .serializers import UserProfileSerializer, UserDocumentSerializer


# Create a new user profile (if it doesn't exist)
class UserProfileCreateView(generics.CreateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically associate the authenticated user with the profile
        serializer.save(user=self.request.user)


# Ensure the user is authenticated and retrieve their own profile
class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        # Return the user profile of the authenticated user
        return UserProfile.objects.get(user=self.request.user)


class UserDocumentListCreateAPIView(generics.ListCreateAPIView):
    queryset = UserDocument.objects.all()
    serializer_class = UserDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]  # Ensure the user is authenticated

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Set the user field to the authenticated user


class UserDocumentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserDocument.objects.all()
    serializer_class = UserDocumentSerializer