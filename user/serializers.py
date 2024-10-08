from rest_framework import serializers
from .models import UserProfile, UserDocument


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'profile_pic',
            'template', 'membership', 'theme', 'notifications',
            'prefered_language', 'prefered_lawyer', 'email_notifications'
        ]


class UserDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDocument
        fields = ['selected_lawyer', 'title', 'base64_content', 'pdf_url', 'template']
        # We don't include 'user' here because we handle it in the view

    def create(self, validated_data):
        # Automatically set the user field before saving
        user = validated_data.pop('user', None)  # This will not be provided, so it's okay
        return UserDocument.objects.create(user=self.context['request'].user, **validated_data)
