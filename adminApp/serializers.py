from rest_framework import serializers
from .models import Template, Category, SubCategory


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'name']


class CategorySerializer(serializers.ModelSerializer):
    sub_categories = SubCategorySerializer(many=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'sub_categories']

    def create(self, validated_data):
        # Extract subcategories data
        sub_categories_data = validated_data.pop('sub_categories', [])
        # Create the category first
        category = Category.objects.create(**validated_data)
        # Create subcategories linked to the category
        for sub_category_data in sub_categories_data:
            SubCategory.objects.create(category=category, **sub_category_data)
        return category

    def update(self, instance, validated_data):
        # Clear subcategories and re-create (or update accordingly)
        sub_categories_data = validated_data.pop('sub_categories', [])
        instance.name = validated_data.get('name', instance.name)
        instance.save()

        # Optionally handle updating subcategories
        instance.sub_categories.all().delete()  # Clear old subcategories
        for sub_category_data in sub_categories_data:
            SubCategory.objects.create(category=instance, **sub_category_data)

        return instance


class TemplateSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    SubCategory = SubCategorySerializer()

    class Meta:
        model = Template
        fields = ['id', 'name', 'category', 'SubCategory', 'questions', 'content', 'created_at']

    def create(self, validated_data):
        return Template.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.category = validated_data.get('category', instance.category)
        instance.SubCategory = validated_data.get('SubCategory', instance.SubCategory)
        instance.questions = validated_data.get('questions', instance.questions)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance
    
