from rest_framework import generics, permissions
from .serializers import UserProfileSerializer


class UserProfileDetailUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile
