from rest_framework import serializers
from .models import Template, Category


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name', 'sub_categories']
    
    
class TemplateSerializer(serializers.ModelSerializer):
    
    category = CategorySerializer()
    
    class Meta:
        model = Template
        fields = ['id', 'name', 'category', 'questions', 'content']
