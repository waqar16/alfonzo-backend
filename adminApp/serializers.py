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
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), write_only=True)
    SubCategory = serializers.PrimaryKeyRelatedField(queryset=SubCategory.objects.all(), write_only=True)

    class Meta:
        model = Template
        fields = ['id', 'name', 'category', 'SubCategory', 'questions', 'content', 'created_at']
        read_only_fields = ['created_at']

    def to_representation(self, instance):
        # Customize the output for GET requests
        representation = super().to_representation(instance)
        representation['category'] = CategorySerializer(instance.category).data
        representation['SubCategory'] = SubCategorySerializer(instance.SubCategory).data
        return representation

    def create(self, validated_data):
        # Extract category and subcategory IDs
        category_id = validated_data.pop('category')
        subcategory_id = validated_data.pop('SubCategory')
        
        # Get the actual instances
        validated_data['category'] = Category.objects.get(id=category_id)
        validated_data['SubCategory'] = SubCategory.objects.get(id=subcategory_id)
        
        return Template.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Extract category and subcategory IDs
        category_id = validated_data.pop('category', None)
        subcategory_id = validated_data.pop('SubCategory', None)

        # Update only if provided
        if category_id is not None:
            instance.category = Category.objects.get(id=category_id)
        if subcategory_id is not None:
            instance.SubCategory = SubCategory.objects.get(id=subcategory_id)

        instance.name = validated_data.get('name', instance.name)
        instance.questions = validated_data.get('questions', instance.questions)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance