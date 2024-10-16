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
    # Nested category and subcategory serializers
    category = CategorySerializer()
    sub_category = SubCategorySerializer()  # Use lowercase 'sub_category' for consistency

    class Meta:
        model = Template
        fields = ['id', 'name', 'category', 'sub_category', 'questions', 'content']

    def create(self, validated_data):
        # Extract the nested category data
        category_data = validated_data.pop('category')
        sub_category_data = validated_data.pop('sub_category')  # Extract subcategory data

        # Create or get the category object
        category, _ = Category.objects.get_or_create(**category_data)

        # Create or get the subcategory object
        sub_category, _ = SubCategory.objects.get_or_create(**sub_category_data)

        # Create the Template with the associated category and subcategory
        template = Template.objects.create(category=category, sub_category=sub_category, **validated_data)
        return template

    def update(self, instance, validated_data):
        # Extract the nested category data
        category_data = validated_data.pop('category')
        sub_category_data = validated_data.pop('sub_category')  # Extract subcategory data

        # Update or create the category
        category, _ = Category.objects.get_or_create(**category_data)

        # Update or create the subcategory
        sub_category, _ = SubCategory.objects.get_or_create(**sub_category_data)

        # Update the Template instance
        instance.category = category
        instance.sub_category = sub_category  # Update the subcategory
        instance.name = validated_data.get('name', instance.name)
        instance.questions = validated_data.get('questions', instance.questions)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance