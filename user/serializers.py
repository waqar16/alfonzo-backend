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


class UserDocumentSerializer(serializers.Serializer):
    class Meta:
        model = UserDocument
        fields = '__all__'
    
    def create(self, validated_data):
        # Create and return a new UserDocument instance, given the validated data
        return UserDocument.objects.create(**validated_data)
