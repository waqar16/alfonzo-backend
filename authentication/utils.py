from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from django.conf import settings
import requests
from django.contrib.auth import get_user_model
import random
from django.core.mail import send_mail
import pyotp
from twilio.rest import Client

User = get_user_model()


def send_sms(to, message):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    client.messages.create(
        body=message,
        from_=settings.TWILIO_PHONE_NUMBER,
        to=to
    )


def send_mfa_code(user):
    # Generate a random 6-digit code
    mfa_code = str(random.randint(100000, 999999))
    
    if user.mfa_method == 'email':
        # Send the MFA code via email
        subject = "Your MFA Code"
        message = f"Your MFA code is: {mfa_code}"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]

        send_mail(subject, message, from_email, recipient_list)

        # Save the code in the user profile for later verification
        user.mfa_code = mfa_code  # You'll need to add a field for mfa_code in your user model
        user.save()

    elif user.mfa_method == 'sms':
        # Logic to send code via SMS
        # Example: using Twilio or similar service
        send_sms(user.phone_number, f"Your MFA code is: {mfa_code}")  # You need to implement send_sms

        # Save the code in the user profile for later verification
        user.mfa_code = mfa_code
        user.save()

    elif user.mfa_method == 'authenticator':
        # Generate a TOTP token and send it to the user (e.g., via email or SMS)
        totp = pyotp.TOTP(user.totp_secret)  # Assumes you have stored a TOTP secret in the user profile
        mfa_code = totp.now()  # This will generate the current TOTP code

        # You can choose how to send the TOTP code to the user
        send_mail(subject, f"Your TOTP code is: {mfa_code}", from_email, recipient_list)

        # Optionally, store the TOTP secret in the user's profile if not done already
        # user.totp_secret = generate_totp_secret()  # You need to implement this
        user.save()


def verify_email_code(user, code):
    # Compare the code from the user with the stored MFA code
    return user.mfa_code == code


def verify_sms_code(user, code):
    # Compare the code from the user with the stored MFA code
    return user.mfa_code == code


def verify_totp_code(user, code):
    # Create a TOTP object and verify the code
    totp = pyotp.TOTP(user.totp_secret)
    return totp.verify(code)


def get_google_user_info(access_token):
    # Google endpoint to verify and fetch user info
    url = 'https://www.googleapis.com/oauth2/v3/userinfo'

    # Send a GET request with the access token
    response = requests.get(url, headers={'Authorization': f'Bearer {access_token}'})

    if response.status_code != 200:
        raise ValueError('Invalid access token')

    # Return user info as a dictionary
    return response.json()


def generate_unique_username(base_username):
    # Start with the base username (before @)
    username = base_username
    counter = 1

    # Keep appending numbers to the username until it's unique
    while User.objects.filter(username=username).exists():
        username = f"{base_username}{counter}"
        counter += 1

    return username


def send_activation_email(user):
    """
    Sends an activation email to the user with an activation link.
    """
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    activation_link = f"http://127.0.0.1:8000/auth/activate/{uid}/{token}/"

    subject = 'Activate your account'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [user.email]

    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
        <div style="max-width: 600px; margin: auto; background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);">
            <h2 style="text-align: center; color: #333;">Welcome back, {user.username}!</h2>
            <p style="text-align: center; color: #555;">Your account is currently inactive. Please click the button below to activate your account:</p>
            <div style="text-align: center;">
                <a href="{activation_link}" style="background-color: #4CAF50; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; font-size: 16px;">Activate your account</a>
            </div>
            <p style="text-align: center; color: #555; margin-top: 20px;">
                If the button above doesn't work, copy and paste the following link in your browser:
            </p>
            <p style="text-align: center; color: #555;">{activation_link}</p>
            <p style="text-align: center; color: #555; margin-top: 30px;">Thank you for reactivating your account!</p>
        </div>
    </body>
    </html>
    """

    # Send the email
    email = EmailMessage(subject, html_content, from_email, to_email)
    email.content_subtype = "html"
    email.send()


def send_password_reset_email(user):
    """
    Sends a password reset email to the user with a reset link.
    """
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    reset_link = f"http://127.0.0.1:8000/auth/password-reset/{uid}/{token}/"

    subject = 'Reset your password'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [user.email]

    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
        <div style="max-width: 600px; margin: auto; background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);">
            <h2 style="text-align: center; color: #333;">Welcome back, {user.username}!</h2>
            <p style="text-align: center; color: #555;">Please click the button below to reset your password:</p>
            <div style="text-align: center;">
                <a href="{reset_link}" style="background-color: #4CAF50; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; font-size: 16px;">Reset your password</a>
            </div>
            <p style="text-align: center; color: #555; margin-top: 20px;">
                If the button above doesn't work, copy and paste the following link in your browser:
            </p>
            <p style="text-align: center; color: #555;">{reset_link}</p>
            <p style="text-align: center; color: #555; margin-top: 30px;">Thank you for resetting your password!</p>
        </div>
    </body>
    </html>
    """

    # Send the email
    email = EmailMessage(subject, html_content, from_email, to_email)
    email.content_subtype = "html"
    email.send()
