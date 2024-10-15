from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=255)
    sub_categories = models.ArrayField(models.CharField(max_length=100), blank=True)

    def __str__(self):
        return self.name


class Template(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    questions = models.JSONField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
