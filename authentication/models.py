from django.contrib.auth.models import AbstractUser
from django.db import models


CHOICES = (("ADMIN", "Admin"), ("USER", "User"), ("LAWYER", "Lawyer"), ("AUDITOR", "Auditor"))


# Custom User Model
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, max_length=255)
    phone = models.CharField(max_length=255, null=True, unique=True, blank=True)
    role = models.CharField(choices=CHOICES, max_length=255, default="USER")
    mfa_enabled = models.BooleanField(default=True)
    mfa_method = models.CharField(max_length=20, choices=[
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('authenticator', 'Authenticator App')
    ], null=True, blank=True, default='authenticator')
    mfa_code = models.CharField(max_length=6, null=True, blank=True)

    def __str__(self):
        return self.username