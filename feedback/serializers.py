from rest_framework import serializers
from .models import Feedback


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id', 'user', 'feedback', 'stars']  # Include the fields you want to expose

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user  # Automatically assign the logged-in user
        return super().create(validated_data)