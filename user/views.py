from rest_framework import generics, permissions, status
from .models import UserProfile, UserDocument
from .serializers import UserProfileSerializer, UserDocumentSerializer, LawyerVerificationUpdateSerializer
from rest_framework.exceptions import PermissionDenied, NotFound, ValidationError
from rest_framework.response import Response


# Create a new user profile (if it doesn't exist)
class UserProfileCreateView(generics.CreateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        try:
            # Automatically associate the authenticated user with the profile
            serializer.save(user=self.request.user)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Ensure the user is authenticated and retrieve their own profile
class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    # permission_classes = [permissions.AllowAny]

    def get_object(self):
        try:
            # Return the user profile of the authenticated user
            return UserProfile.objects.get(user=self.request.user)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, *args, **kwargs):
        # Handle PATCH request for updating the UserProfile
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)
    
    def put(self, request, *args, **kwargs):
        # Handle PUT request for updating the UserProfile
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def handle_exception(self, exc):
        if isinstance(exc, PermissionDenied):
            return Response({'error': 'Permission Denied'}, status=status.HTTP_403_FORBIDDEN)
        elif isinstance(exc, NotFound):
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
        return super().handle_exception(exc)


class UserDocumentListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = UserDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        try:
            # Return only the documents created by the authenticated user
            return UserDocument.objects.filter(user=self.request.user)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)  # Set the user field to the authenticated user
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserDocumentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserDocument.objects.all()
    serializer_class = UserDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def handle_exception(self, exc):
        if isinstance(exc, NotFound):
            return Response({'error': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)
        elif isinstance(exc, PermissionDenied):
            return Response({'error': 'Permission Denied'}, status=status.HTTP_403_FORBIDDEN)
        return super().handle_exception(exc)


class LawyerUpdateVerificationAPIView(generics.UpdateAPIView):
    queryset = UserDocument.objects.all()
    serializer_class = LawyerVerificationUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]  # Ensure the lawyer is authenticated

    def get_queryset(self):
        try:
            """
            Restrict the queryset to documents where the current user is the selected lawyer.
            """
            return UserDocument.objects.filter(selected_lawyer__user=self.request.user)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)