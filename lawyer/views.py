from rest_framework import generics, permissions
from .serializers import LawyerProfileSerializer


class LawyerProfileDetailUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = LawyerProfileSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        return self.request.user.profile
