from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from .models import UserProfile, UserDocument
from .serializers import UserProfileSerializer, UserDocumentSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets


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


class UserDocumentViewSet(viewsets.ModelViewSet):
    queryset = UserDocument.objects.all()
    serializer_class = UserDocumentSerializer

class UserDocumentCreateView(generics.CreateAPIView):
    """
    Create a new UserDocument instance.
    """
    serializer_class = UserDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Save the new document with the currently logged-in user.
        """
        # Assign the user from the request
        serializer.save(user=self.request.user)
        
    def create(self, request, *args, **kwargs):
        # Print incoming data for debugging
        print("Request data:", request.data)
        
        # Create the UserDocument
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("Validation errors:", serializer.errors)  # Debugging
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



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
