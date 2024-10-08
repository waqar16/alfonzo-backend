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


class UserDocumentListCreateView(generics.ListCreateAPIView):
    """
    List all user documents or create a new document.
    """
    serializer_class = UserDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]




class UserDocumentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a user document.
    """
    serializer_class = UserDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """
        Retrieve the document while ensuring the user owns it.
        """
        obj = get_object_or_404(UserDocument, pk=self.kwargs['pk'])
        if obj.user != self.request.user:
            raise permissions.PermissionDenied("You do not have permission to access this document.")
        return obj
