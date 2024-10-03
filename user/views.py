from rest_framework import generics, permissions
from .models import UserProfile
from .serializers import UserProfileSerializer


# Ensure the user is authenticated and retrieve their own profile
class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Return the user profile of the authenticated user
        return UserProfile.objects.get(user=self.request.user)
