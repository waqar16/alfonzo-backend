from rest_framework import serializers
from .models import LawyerProfile, LawyerDocument, UserQuery
from user.models import UserDocument


class LawyerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = LawyerProfile
        fields = '__all__'

    def create(self, validated_data):
        # Create and return a new LawyerDocument instance, given the validated data
        return LawyerDocument.objects.create(**validated_data)


class LawyerDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LawyerDocument
        fields = ['selected_lawyer', 'title', 'base64_content', 'pdf_url', 'template', 'verification_status']
        # We don't include 'user' here because we handle it in the view

    def create(self, validated_data):
        # Automatically set the user field before saving
        """
        Automatically set the user field to the current user before saving
        """
        validated_data.pop('user', None)  # This will not be provided, so it's okay
        return LawyerDocument.objects.create(
            user=self.context['request'].user,
            **validated_data
        )


class UserQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserQuery
        fields = '__all__'

    def create(self, validated_data):
        # Automatically set the user when creating a new query
        request = self.context['request']
        user = request.user
        return UserQuery.objects.create(user=user, **validated_data)


class LawyerVerificationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LawyerDocument
        fields = ['verification_status']  # Only allow updating verification status


class UserDocumentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDocument
        fields = '__all__'


class LawyerDocumentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = LawyerDocument
        fields = '__all__'
