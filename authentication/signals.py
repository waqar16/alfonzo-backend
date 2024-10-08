from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from user.models import UserProfile
from lawyer.models import LawyerProfile

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
        elif instance.role == 'Lawyer':
            LawyerProfile.objects.create(
                user=instance,
                first_name=instance.first_name,
                last_name=instance.last_name,
                email=instance.email,
                phone=instance.phone,
            )

# Automatically save the profile when the user is updated
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    if instance.role == 'User' and hasattr(instance, 'user_profile'):
        instance.user_profile.save()
    elif instance.role == 'Lawyer' and hasattr(instance, 'lawyer_profile'):
        instance.lawyer_profile.save()
