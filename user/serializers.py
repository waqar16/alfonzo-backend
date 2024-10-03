from rest_framework import serializers
from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'profile_pic',
            'template', 'membership', 'theme', 'notifications',
            'prefered_language', 'prefered_lawyer', 'email_notifications'
        ]
