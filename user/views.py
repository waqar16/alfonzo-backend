from rest_framework import generics, permissions
from .models import UserProfile, UserDocument
from .serializers import UserProfileSerializer, UserDocumentSerializer, LawyerVerificationUpdateSerializer


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


class UserDocumentListCreateAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Return only the documents created by the authenticated user
        return UserDocument.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Set the user field to the authenticated user


class UserDocumentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserDocument.objects.all()
    serializer_class = UserDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]


class LawyerUpdateVerificationAPIView(generics.UpdateAPIView):
    queryset = UserDocument.objects.all()
    serializer_class = LawyerVerificationUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]  # Ensure the lawyer is authenticated

    def get_queryset(self):
        """
        Restrict the queryset to documents where the current user is the selected lawyer.
        """
        return UserDocument.objects.filter(selected_lawyer__user=self.request.user)