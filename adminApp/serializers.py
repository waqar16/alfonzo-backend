from rest_framework import serializers
from .models import Template, Category, SubCategory


class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = '__all__'


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'category'] 


class CategorySerializer(serializers.ModelSerializer):
    sub_categories = SubCategorySerializer(many=True, read_only=True, source='sub_category')

    class Meta:
        model = Category
        fields = ['id', 'name', 'sub_categories']