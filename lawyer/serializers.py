from rest_framework import serializers
from .models import LawyerProfile


class LawyerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = LawyerProfile
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'profile_pic',
            'template', 'membership', 'theme', 'notifications',
            'prefered_language', 'email_notifications'
        ]
