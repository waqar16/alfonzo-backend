from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from user.models import UserProfile
from lawyer.models import LawyerProfile
from notification.models import Notification
from user.models import UserDocument
from lawyer.models import LawyerDocument

User = get_user_model()


# Automatically create the profile when the user is created
@receiver(post_save, sender=User)
def create_profile_based_on_role(sender, instance, created, **kwargs):
    if created:
        # Check the user's role and create the corresponding profile
        if instance.role == 'User':
            UserProfile.objects.create(
                user=instance,
                first_name=instance.first_name,
                last_name=instance.last_name,
                email=instance.email,
                phone=instance.phone,
            )
            create_notification(instance, "Profile created", f"Your user profile has been created successfully. Welcome {instance.first_name}!")
        elif instance.role == 'Lawyer':
            LawyerProfile.objects.create(
                user=instance,
                first_name=instance.first_name,
                last_name=instance.last_name,
                email=instance.email,
                phone=instance.phone,
            )
            create_notification(instance, "Profile created", f"Your lawyer profile has been created successfully. Welcome {instance.first_name}!")


# Automatically save the profile when the user is updated
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    if instance.role == 'User' and hasattr(instance, 'user_profile'):
        instance.user_profile.save()
    elif instance.role == 'Lawyer' and hasattr(instance, 'lawyer_profile'):
        instance.lawyer_profile.save()


def create_notification(user_instance, title, message):
    Notification.objects.create(
        user=user_instance,
        title=title,
        message=message,
    )


@receiver(post_save, sender=UserDocument)
def create_notification_on_document_upload(sender, instance, created, **kwargs):
    if created:
        create_notification(instance.user, "Document Created Successfully", f"Your document has been created successfully.")



@receiver(post_save, sender=LawyerDocument)
def create_notification_on_document_upload(sender, instance, created, **kwargs):
    if created:
        create_notification(instance.user, "Document Created Successfully", f"Your document has been created successfully.")