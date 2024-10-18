from rest_framework import serializers
from .models import UserProfile, UserDocument


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"


class UserDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDocument
        fields = ['id', 'selected_lawyer', 'title', 'base64_content', 'content', 'pdf_url', 'template', 'verification_status']
        # We don't include 'user' here because we handle it in the view

    def create(self, validated_data):
        # Automatically set the user field before saving
        """
        Automatically set the user field to the current user before saving
        """
        validated_data.pop('user', None)  # This will not be provided, so it's okay
        return UserDocument.objects.create(
            user=self.context['request'].user,
            **validated_data
        )
    

class LawyerVerificationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDocument
        fields = ['verification_status']  # Only allow updating verification status
