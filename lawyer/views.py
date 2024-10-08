from rest_framework import generics, permissions
from .serializers import LawyerProfileSerializer
from .models import Lawyerprofile


# Create a new lawyer profile (if it doesn't exist)
class UserProfileCreateView(generics.CreateAPIView):
    serializer_class = LawyerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically associate the authenticated user with the profile
        serializer.save(user=self.request.user)


# Retrieve, update or delete a lawyer profile       
class LawyerProfileDetailUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = LawyerProfileSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        # Return the user profile of the authenticated user
        return Lawyerprofile.objects.get(user=self.request.user)