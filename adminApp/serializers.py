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
    sub_categories = SubCategorySerializer(many=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'sub_categories']

    def create(self, validated_data):
        sub_categories_data = validated_data.pop('sub_categories', [])
        category = Category.objects.create(**validated_data)
        for sub_category_data in sub_categories_data:
            SubCategory.objects.create(category=category, **sub_category_data)
        return category