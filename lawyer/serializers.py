from rest_framework import serializers
from .models import LawyerProfile, LawyerDocument


class LawyerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = LawyerProfile
        fields = '__all__'
 
    def create(self, validated_data):
        # Create and return a new UserDocument instance, given the validated data
        return LawyerDocument.objects.create(**validated_data)
