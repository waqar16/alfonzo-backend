from rest_framework import generics, permissions
from .serializers import (LawyerProfileSerializer,
                          LawyerDocumentSerializer,
                          UserQuerySerializer,
                          LawyerVerificationUpdateSerializer,
                          UserDocumentListSerializer,
                          LawyerDocumentListSerializer
                          )
from .models import LawyerProfile, LawyerDocument, UserQuery
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from user.models import UserDocument
from rest_framework.response import Response


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


class LawyerDocumentListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = LawyerDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Return only the documents created by the authenticated user
        return LawyerDocument.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Set the user field to the authenticated user


class LawyerDocumentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LawyerDocument.objects.all()
    serializer_class = LawyerDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]


class SendQueryToLawyerAPIView(generics.ListCreateAPIView):
    queryset = UserQuery.objects.all()
    serializer_class = UserQuerySerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can send queries

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Set the authenticated user as the sender


class LawyerUpdateVerificationAPIView(generics.UpdateAPIView):
    queryset = LawyerDocument.objects.all()
    serializer_class = LawyerVerificationUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]  # Ensure the lawyer is authenticated

    def get_queryset(self):
        """
        Restrict the queryset to documents where the current user is the selected lawyer.
        """
        return LawyerDocument.objects.filter(selected_lawyer__user=self.request.user)


class CombinedDocumentsListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]  # Ensure the lawyer is authenticated

    def get_queryset(self):
        """
        Retrieve documents from both UserDocument and LawyerDocument where the current user is the selected lawyer.
        """
        user_documents = UserDocument.objects.filter(selected_lawyer__user=self.request.user)
        lawyer_documents = LawyerDocument.objects.filter(user=self.request.user)  # Use user instead of lawyer

        return user_documents, lawyer_documents  # Return both querysets separately

    def get(self, request, *args, **kwargs):
        user_documents, lawyer_documents = self.get_queryset()

        user_documents_data = UserDocumentListSerializer(user_documents, many=True).data
        lawyer_documents_data = LawyerDocumentListSerializer(lawyer_documents, many=True).data

        # Combine the data into a single response
        combined_data = {
            'user_documents': user_documents_data,
            'lawyer_documents': lawyer_documents_data
        }

        return Response(combined_data)

    def get_serializer_class(self):
        """
        Return the appropriate serializer class based on the document type.
        """
        # You can customize this if you want to switch between serializers based on a query parameter
        return UserDocumentListSerializer if self.request.GET.get('type') == 'user' else LawyerDocumentListSerializer