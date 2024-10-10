from django.utils import timezone 
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import RegisterSerializer, MyTokenObtainPairSerializer
from .serializers import UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from .utils import get_google_user_info, generate_unique_username
from .utils import send_password_reset_email, verify_email_code
from .utils import verify_sms_code, verify_totp_code
from .utils import send_activation_email
from rest_framework_simplejwt.tokens import RefreshToken
import requests
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.hashers import check_password
from user.models import UserDevice, UserProfile


User = get_user_model()


# Google Login
class GoogleLoginAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        access_token = request.data.get("access_token")

        if not access_token:
            return Response({"error": "Access token is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Step 1: Verify the Google access token and get user info
        google_user_info = get_google_user_info(access_token)

        email = google_user_info.get('email')
        first_name = google_user_info.get('given_name')
        last_name = google_user_info.get('family_name')
        profile_picture = google_user_info.get('picture')

        # Step 2: Check if the user exists in the database, if not create a new user
        user = User.objects.get(email=email)
    
        if user:
            if user.has_usable_password():
                return Response(
                    {"error": "It looks like your account is not linked with Google. Please login with the same email and password you set while creating account."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            user = User.objects.create(
                username=generate_unique_username(email.split('@')[0]),
                email=email,
                first_name=first_name,
                last_name=last_name,
                is_active=True
            )
            user.set_unusable_password()
            user.save()
            
            user_profile = UserProfile.objects.create(
                user=user,
                first_name=first_name,
                last_name=last_name,
                email=email,
                profile_pic=profile_picture
            )
            user_profile.save()

        # Step 3: Issue JWT token for the user
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "profile_picture": profile_picture
            }
        })


# LinkedIn OAuth
class LinkedInCallbackView(APIView):
    """
    Handle LinkedIn OAuth callback.
    """

    permission_classes = [AllowAny]

    def get(self, request):
        code = request.GET.get('code')

        if not code:
            return Response({"error": "Authorization code not provided"}, status=400)

        # Exchange authorization code for access token
        token_data = self.get_access_token(code)
        access_token = token_data.get('access_token')

        if not access_token:
            return Response({"error": "Failed to get access token"}, status=400)

        # Fetch user profile data from LinkedIn
        linkedin_user_data = self.get_linkedin_user_info(access_token)
        if not linkedin_user_data:
            return Response({"error": "Failed to fetch user info"}, status=400)
        
        # Extract user data
        email = linkedin_user_data['email']
        first_name = linkedin_user_data['first_name']
        last_name = linkedin_user_data['last_name']
        profile_picture = linkedin_user_data['profile_picture']
        # Handle user creation or retrieval

        try:
            user = User.objects.get(email=email)
            if user.has_usable_password():
                Response({"error": "It looks like your account is not linked with Google. Please login with the same email and password you set while creating account."}, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            user = User.objects.create(
                username=generate_unique_username(email.split('@')[0]),
                email=email,
                first_name=first_name,
                last_name=last_name,
                is_active=True
            )
            user.set_unusable_password()
            user.save()
            
            UserProfile.objects.create(
                user=user,
                first_name=first_name,
                last_name=last_name,
                email=email,
                profile_pic=profile_picture
             )
            UserProfile.save()

        # Create JWT tokens
        refresh = RefreshToken.for_user(user)
        # return Response({
        #     'refresh': str(refresh),
        #     'access': str(refresh.access_token),
        # })
        redirect_url = f"http://127.0.0.1:3000/profile?refresh={str(refresh)}&access={str(refresh.access_token)}"
        return redirect(redirect_url)

    def get_access_token(self, code):
        """
        Exchange authorization code for an access token.
        """
        token_url = "https://www.linkedin.com/oauth/v2/accessToken"
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': settings.LINKEDIN_REDIRECT_URI,
            'client_id': settings.LINKEDIN_CLIENT_ID,
            'client_secret': settings.LINKEDIN_CLIENT_SECRET,
        }
        response = requests.post(token_url, data=data)
        print(response.json())
        return response.json()
    def get_linkedin_user_info(self, access_token):
        """
        Fetch user profile and email from LinkedIn.
        """
        userinfo_url = "https://api.linkedin.com/v2/userinfo"
        headers = {'Authorization': f'Bearer {access_token}'}

        # Get user information
        userinfo_response = requests.get(userinfo_url, headers=headers)
        if userinfo_response.status_code != 200:
            return None

        userinfo_data = userinfo_response.json()

        return {
            'first_name': userinfo_data.get('given_name', ''),
            'last_name': userinfo_data.get('family_name', ''),
            'email': userinfo_data.get('email', ''),
            'profile_picture': userinfo_data.get('picture', ''),
            'locale': userinfo_data.get('locale', ''),
        }


# LinkedIn Login
class LinkedInLoginRedirect(APIView):
    """
    Redirect user to LinkedIn for login.
    """

    permission_classes = [AllowAny]

    def get(self, request):
        linkedin_auth_url = (
            "https://www.linkedin.com/oauth/v2/authorization"
            "?response_type=code"
            f"&client_id={settings.LINKEDIN_CLIENT_ID}"
            f"&redirect_uri={settings.LINKEDIN_REDIRECT_URI}"
            "&scope=openid%20profile%20email"
        )
        return redirect(linkedin_auth_url)


# User Registration View
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Custom Token View for JWT login
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        # Check if MFA is required and return an appropriate response
        if validated_data.get('mfa_required'):
            # Get the user object from the validated_data (user_obj from serializer)
            user = validated_data.get('user')
            if user:
                email = user.email
                username = user.username
                first_name = user.first_name
                last_name = user.last_name
                return Response({
                    'message': validated_data['message'],
                    'mfa_required': True,
                    'email': email,
                    'username': username,
                    'first_name': first_name,
                    'last_name': last_name
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'detail': 'User data is missing.'
                }, status=status.HTTP_400_BAD_REQUEST)

        # Return JWT tokens and user info if authentication is successful
        return Response(validated_data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# User Profile Data View
class LoggedInUserView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is logged in
    def get(self, request, *args, **kwargs):
        # Get the logged-in user (from the request object)
        user = request.user
        # Serialize the user object
        serializer = UserSerializer(user)
        # Return the serialized data
        return Response(serializer.data)


# Activate Account View
class ActivateAccountView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            # Decode the user ID from the URL-safe base64 string
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            # return Response({'status': 'Account activated successfully'}, status=status.HTTP_200_OK)
            return redirect(f"{settings.FRONTEND_BASE_URL}/login?activationStatus=success")
        else:
            return redirect(f"{settings.FRONTEND_BASE_URL}/activation-email-sent?activationStatus=failed")
 

# Deactivate Account View
class DeactivateAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user.is_active = False
        user.save()
        return Response({'status': 'Account deactivated successfully'}, status=status.HTTP_200_OK)


# Auth Guard View
class AuthGuardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_authenticated:
            return Response({'message': 'User is authenticated', 'role': request.user.role}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)  


# Reset Password Link View
class ResetPasswordLinkView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()
        if user:
            if not user.has_usable_password():
                return Response({'error': 'Cannot reset password beacuse account use social login'}, status=status.HTTP_400_BAD_REQUEST)
            send_password_reset_email(user)
            return Response({'message': 'Password reset link sent to your email.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


# Reset Password View
class ResetPasswordView(APIView):
    """
    Handles the password reset process by validating the uid and token,
    checking the current password, and updating it with the new password.
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        # uidb64 = data.get('uid')
        # token = data.get('token')
        current_password = data.get('current_password')
        new_password = data.get('new_password')

        if not (current_password and new_password):
            return Response({'error': 'All fields are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Decode the user ID
        # try:
        #     uid = urlsafe_base64_decode(uidb64).decode()
        #     user = User.objects.get(pk=uid)
        # except (User.DoesNotExist, ValueError, TypeError):
        #     return Response({'error': 'Invalid user ID.'}, status=status.HTTP_400_BAD_REQUEST)

        # Verify the token
        # if not default_token_generator.check_token(user, token):
        #     return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)

        # Verify the current password
        if not check_password(current_password, user.password):
            return Response({'error': 'Incorrect current password.'}, status=status.HTTP_400_BAD_REQUEST)

        # Set the new password
        user.set_password(new_password)
        user.save()

        return Response({'success': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)


# Change Username View
class ChangeUsernameView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        new_username = request.data.get('username')
        
        # Ensure the new username is provided
        if not new_username:
            return Response({'error': 'New username is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if the new username is already taken
        if User.objects.filter(username=new_username).exists():
            return Response({'error': 'Username is already taken'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Update the username of the authenticated user
        user = request.user
        user.username = new_username
        user.save()

        return Response({'message': 'Username successfully updated'}, status=status.HTTP_200_OK)


# Resend Activation Email View
class ResendActivationEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()
        if user:
            send_activation_email(user)
            return Response({'message': 'Activation email sent to your email.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


# MFA Settings View
class MFASettingsView(APIView):
    def post(self, request):
        user = request.user
        mfa_method = request.data.get('mfa_method')
        phone = request.data.get('phone')

        # Check if the provided MFA method is valid
        if mfa_method not in ['email', 'sms', 'authenticator']:
            return Response({'error': 'Invalid MFA method'}, status=status.HTTP_400_BAD_REQUEST)

        # If MFA method is SMS, ensure phone is either in the request or already exists on the user object
        if mfa_method == 'sms':
            # Check if phone is in the request body or already exists on the user profile
            if not phone and not user.phone:
                return Response({'error': 'Phone is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            # If phone is in the request body, update the user's phone number
            if phone:
                user.phone = phone
            
            user.mfa_method = mfa_method
            user.mfa_enabled = True
            user.save()

        elif mfa_method == 'authenticator':
            user.mfa_method = mfa_method
            user.mfa_enabled = True
            user.save()
        
        else:
            # For email MFA or any other method
            user.mfa_method = mfa_method
            user.mfa_enabled = True
            user.save()
            
        return Response({'message': f'MFA method updated to {mfa_method}'}, status=status.HTTP_200_OK)


# Verify MFA View
class VerifyMFAView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        mfa_code = request.data.get('mfa_code')

        user = User.objects.get(email=email)

        if user.mfa_method == 'email':
            # Logic to verify email code
            if verify_email_code(user, mfa_code):  # Implement verify_email_code function
                user.mfa_enabled = False
                user.save()
                device_identifier = request.META['HTTP_USER_AGENT']
                UserDevice.objects.update_or_create(
                    user=user,
                    device_identifier=device_identifier,
                    defaults={'last_login': timezone.now()}
                )
                refresh = RefreshToken.for_user(user)
                data = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
                return Response(data, status=status.HTTP_200_OK)
        elif user.mfa_method == 'sms':
            # Logic to verify SMS code
            if verify_sms_code(user, mfa_code):  # Implement verify_sms_code function
                user.mfa_enabled = False
                user.save()
                device_identifier = request.META['HTTP_USER_AGENT']
                UserDevice.objects.update_or_create(
                    user=user,
                    device_identifier=device_identifier,
                    defaults={'last_login': timezone.now()}
                )
                refresh = RefreshToken.for_user(user)
                data = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
                return Response(data, status=status.HTTP_200_OK)

        elif user.mfa_method == 'authenticator':
            if verify_totp_code(user, mfa_code):
                user.mfa_enabled = False
                user.save()
                device_identifier = request.META['HTTP_USER_AGENT']
                UserDevice.objects.update_or_create(
                    user=user,
                    device_identifier=device_identifier,
                    defaults={'last_login': timezone.now()}
                )
                refresh = RefreshToken.for_user(user)
                data = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
                return Response(data, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid MFA code or may be exipred if you are using TOTP'}, status=status.HTTP_400_BAD_REQUEST)
