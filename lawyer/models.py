from django.db import models
from django.contrib.auth import get_user_model
from adminApp.models import Template

User = get_user_model()


class LawyerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='lawyer_profile')
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255,null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    profile_pic = models.URLField(null=True, blank=True)
    template = models.ForeignKey(Template, on_delete=models.CASCADE, null=True, blank=True)
    membership = models.BooleanField(default=False)
    theme = models.CharField(max_length=255, default="dark")
    notifications = models.BooleanField(default=True)
    prefered_language = models.CharField(max_length=255, default="en")
    email_notifications = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username


class LawyerDocument(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    selected_lawyer = models.ForeignKey(
        LawyerProfile,
        on_delete=models.CASCADE,
        related_name="preferred_lawyer_documents",
    )
    title = models.CharField(max_length=255)
    base64_content = models.TextField()
    content = models.TextField(null=True, blank=True)
    pdf_url = models.URLField(null=True, blank=True)
    template = models.ForeignKey(Template, on_delete=models.CASCADE, blank=True, null=True)
    verification_status = models.CharField(max_length=255, default="Not Specified", choices=[
        ('Not Specified', 'Not Specified'),
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected ', 'Rejected'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.user.username}"


class UserQuery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="queries")
    lawyer = models.ForeignKey(LawyerProfile, on_delete=models.CASCADE, related_name="queries_received")
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Query from {self.user.username} to {self.lawyer.user.username} at {self.timestamp}"


class LawyerApproval(models.Model):
    lawyer = models.ForeignKey('LawyerProfile', on_delete=models.CASCADE)
    user_documents = models.ManyToManyField('user.UserDocument', blank=True)  # Use string reference
    lawyer_documents = models.ManyToManyField('lawyer.LawyerDocument', blank=True)  # Use string reference
    status = models.CharField(max_length=255, default="Pending", choices=[
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected')
    ])

    def __str__(self):
        return f"{self.lawyer} - {self.status}"
