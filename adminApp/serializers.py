class TemplateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    sub_category = serializers.PrimaryKeyRelatedField(queryset=SubCategory.objects.all())  # Removed source

    class Meta:
        model = Template
        fields = ['id', 'name', 'category', 'sub_category', 'questions', 'content', 'created_at']

    def create(self, validated_data):
        category_id = validated_data.pop('category')
        sub_category_id = validated_data.pop('sub_category', None)

        # Use category_id and sub_category_id directly since they are integers (PKs)
        validated_data['category'] = Category.objects.get(id=category_id)
        if sub_category_id:
            validated_data['sub_category'] = SubCategory.objects.get(id=sub_category_id)

        return Template.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.category = validated_data.get('category', instance.category)
        instance.sub_category = validated_data.get('sub_category', instance.sub_category)  # Fixed to sub_category
        instance.questions = validated_data.get('questions', instance.questions)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = {
            'id': instance.category.id,
            'name': instance.category.name,
            'sub_categories': [{'id': sub.id, 'name': sub.name} for sub in instance.category.sub_categories.all()]
        }
        representation['sub_category'] = {
            'id': instance.sub_category.id,
            'name': instance.sub_category.name
        } if instance.sub_category else None
        return representation