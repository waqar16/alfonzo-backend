# from rest_framework import serializers
# from .models import Template, Category, SubCategory


# class SubCategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SubCategory
#         fields = ['id', 'name']


# class CategorySerializer(serializers.ModelSerializer):
#     sub_categories = SubCategorySerializer(many=True)

#     class Meta:
#         model = Category
#         fields = ['id', 'name', 'sub_categories']

#     def create(self, validated_data):
#         sub_categories_data = validated_data.pop('sub_categories', [])
#         category = Category.objects.create(**validated_data)
#         for sub_category_data in sub_categories_data:
#             SubCategory.objects.create(category=category, **sub_category_data)
#         return category

#     def update(self, instance, validated_data):
#         sub_categories_data = validated_data.pop('sub_categories', [])
#         instance.name = validated_data.get('name', instance.name)
#         instance.save()

#         # Clear old subcategories and create new ones
#         instance.sub_categories.all().delete()
#         for sub_category_data in sub_categories_data:
#             SubCategory.objects.create(category=instance, **sub_category_data)

#         return instance


# class TemplateSerializer(serializers.ModelSerializer):
#     category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
#     sub_category = serializers.PrimaryKeyRelatedField(queryset=SubCategory.objects.all(), source='SubCategory')

#     class Meta:
#         model = Template
#         fields = ['id', 'name', 'category', 'sub_category', 'questions', 'content', 'created_at']

#     def create(self, validated_data):
#         return Template.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.category = validated_data.get('category', instance.category)
#         instance.SubCategory = validated_data.get('sub_category', instance.SubCategory)
#         instance.questions = validated_data.get('questions', instance.questions)
#         instance.content = validated_data.get('content', instance.content)
#         instance.save()
#         return instance


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
        sub_categories_data = validated_data.pop('sub_categories', [])
        category = Category.objects.create(**validated_data)
        for sub_category_data in sub_categories_data:
            SubCategory.objects.create(category=category, **sub_category_data)
        return category

    def update(self, instance, validated_data):
        sub_categories_data = validated_data.pop('sub_categories', [])
        instance.name = validated_data.get('name', instance.name)
        instance.save()

        # Clear old subcategories and create new ones
        instance.sub_categories.all().delete()
        for sub_category_data in sub_categories_data:
            SubCategory.objects.create(category=instance, **sub_category_data)

        return instance


class TemplateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    sub_category = serializers.PrimaryKeyRelatedField(queryset=SubCategory.objects.all(), source='SubCategory')

    class Meta:
        model = Template
        fields = ['id', 'name', 'category', 'sub_category', 'questions', 'content', 'created_at']

    def create(self, validated_data):
        # Extract category and sub_category IDs
        category_id = validated_data.pop('category')
        sub_category_id = validated_data.pop('sub_category', None)  # Correcting to 'sub_category'

        # Retrieve the Category and SubCategory instances
        validated_data['category'] = Category.objects.get(id=category_id)
        if sub_category_id:
            validated_data['SubCategory'] = SubCategory.objects.get(id=sub_category_id)

        return Template.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.category = validated_data.get('category', instance.category)
        instance.SubCategory = validated_data.get('sub_category', instance.SubCategory)  # Correcting to 'sub_category'
        instance.questions = validated_data.get('questions', instance.questions)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Include complete category and sub_category objects
        representation['category'] = {
            'id': instance.category.id,
            'name': instance.category.name,
            'sub_categories': [{'id': sub.id, 'name': sub.name} for sub in instance.category.sub_categories.all()]
        }
        representation['sub_category'] = {
            'id': instance.SubCategory.id,
            'name': instance.SubCategory.name
        } if instance.SubCategory else None
        return representation