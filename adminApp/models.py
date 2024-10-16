from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    """
    A model representing the main category.
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    """
    A model representing subcategories, linked to Category via a ForeignKey.
    """
    category = models.ForeignKey(Category, related_name='sub_categories', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} ({self.category.name})"


class Template(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    SubCategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, blank=True)
    questions = models.JSONField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.name


