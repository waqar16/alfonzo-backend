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
    category_id = serializers.IntegerField(source='category.id')
    sub_category_id = serializers.IntegerField(source='SubCategory.id')

    class Meta:
        model = Template
        fields = ['id', 'name', 'category_id', 'sub_category_id', 'questions', 'content', 'created_at']

    def create(self, validated_data):
        # Extract category and subcategory IDs
        category_id = validated_data.pop('category')['id']
        sub_category_id = validated_data.pop('SubCategory')['id']
        
        # Retrieve the Category and SubCategory instances
        category = Category.objects.get(id=category_id)
        sub_category = SubCategory.objects.get(id=sub_category_id)

        # Create the Template instance with the retrieved instances
        template = Template.objects.create(category=category, SubCategory=sub_category, **validated_data)
        
        return template

    def update(self, instance, validated_data):
        # Similar logic as create to retrieve Category and SubCategory
        category_id = validated_data.get('category', {}).get('id', instance.category.id)
        sub_category_id = validated_data.get('SubCategory', {}).get('id', instance.SubCategory.id)

        instance.name = validated_data.get('name', instance.name)
        instance.questions = validated_data.get('questions', instance.questions)
        instance.content = validated_data.get('content', instance.content)

        # Retrieve and set the Category and SubCategory instances
        instance.category = Category.objects.get(id=category_id)
        instance.SubCategory = SubCategory.objects.get(id=sub_category_id)

        instance.save()
        return instance