from rest_framework import serializers
from .models import LawyerProfile


class LawyerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = LawyerProfile
        fields = '__all__'
