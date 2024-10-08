import os
import django

# Set up the Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alfonzoBackend.settings')  # Replace with your project's settings module
django.setup()

from django.contrib.auth import get_user_model
from user.models import UserProfile
from lawyer.models import LawyerProfile

User = get_user_model()

def create_user_and_profile(username, email, password, role):
    # Create a new user with the provided username, password, and role
    user = User.objects.create_user(username=username, email=email, password=password, role=role)
    print(f"User created with username: {username} and role: {role}")

    # Check if the corresponding profile was created
    if role == 'User':
        if UserProfile.objects.filter(user=user).exists():
            print(f"UserProfile for {username} created successfully.")
        else:
            print(f"UserProfile for {username} was not created.")
    elif role == 'LAWYER':
        if LawyerProfile.objects.filter(user=user).exists():
            print(f"LawyerProfile for {username} created successfully.")
        else:
            print(f"LawyerProfile for {username} was not created.")

if __name__ == "__main__":
    # Test data for user creation
    username = 'war'
    email = 'm6j@example.com'
    password = 'testpass'
    role = 'Lawyer'  # You can change this to 'LAWYER' to test LawyerProfile creation

    create_user_and_profile(username, email, password, role)
