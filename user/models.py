from django.db import models
from django.contrib.auth import get_user_model
from adminApp.models import Template
from lawyer.models import LawyerProfile

User = get_user_model()


# User Profile
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    membership = models.BooleanField(default=False)
    theme = models.CharField(max_length=255, default="dark")
    notifications = models.BooleanField(default=True)
    prefered_language = models.CharField(max_length=255, default="en")
    prefered_lawyer = models.OneToOneField(User, on_delete=models.CASCADE, related_name="prefered_lawyer", null=True, blank=True)
    email_notifications = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username


# Documents model
class UserDocument(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    prefered_lawyer = models.ForeignKey(LawyerProfile, on_delete=models.CASCADE, related_name="preferred_lawyer", null=True, blank=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title + " - " + self.user.user.username


# Device model
class UserDevice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device_identifier = models.CharField(max_length=255)
    last_login = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.device_identifier}"
