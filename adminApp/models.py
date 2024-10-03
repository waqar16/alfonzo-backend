from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Template(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    question = models.TextField(null=True, blank=True)
    content = models.TextField()

    def __str__(self):
        return self.name
