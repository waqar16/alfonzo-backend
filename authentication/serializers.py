from django.utils import timezone
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from .utils import send_activation_email, send_mfa_code
from user.models import UserDevice

User = get_user_model()


# # User Registration Serializer
# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
#     password2 = serializers.CharField(write_only=True, required=True)

#     class Meta:
#         model = User
#         fields = ('username', 'password', 'password2', 'email', 'mfa_method', 'mfa_enabled',)

#     def validate(self, attrs):
#         if attrs['password'] != attrs['password2']:
#             raise serializers.ValidationError({"password": "Password fields didn't match."})
        
#         # Check for unique email and username
#         if User.objects.filter(email=attrs['email']).exists():
#             raise serializers.ValidationError({"email": "A user with that email already exists."})
#         if User.objects.filter(username=attrs['username']).exists():
#             raise serializers.ValidationError({"username": "A user with that username already exists."})
        
#         # Prevent admin and auditor roles from signing up
#         if attrs.get('role') in ['ADMIN', 'AUDITOR']:  # Adjust as per your role constants
#             raise serializers.ValidationError({"role": "Admin and Auditor roles cannot register."})
        
#         return attrs

#     def create(self, validated_data):
#         user = User.objects.create(
#             username=validated_data['username'],
#             email=validated_data['email'],
#             first_name=validated_data['first_name'],
#             last_name=validated_data['last_name'],
#             is_active=False,
#             phone=validated_data['phone'],
#             role=validated_data['role']
#         )
#         user.set_password(validated_data['password'])
#         user.save()

#         # Send activation email
#         send_activation_email(user)

#         return user

CHOICES = (
    ("ADMIN", "Admin"),
    ("USER", "User"),
    ("LAWYER", "Lawyer"),
    ("AUDITOR", "Auditor")
)

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField(required=False, allow_blank=True, default='')
    last_name = serializers.CharField(required=False, allow_blank=True, default='')
    phone = serializers.CharField(required=False, allow_blank=True, default='')
    role = serializers.ChoiceField(choices=CHOICES, required=False, default='USER')
    mfa_method = serializers.ChoiceField(
        choices=[('email', 'Email'), ('sms', 'SMS'), ('totp', 'TOTP')],
        required=False,
        default='email'
    )
    mfa_enabled = serializers.BooleanField(required=False, default=True)

    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'password2',
            'email',
            'mfa_method',
            'mfa_enabled',
            'first_name',
            'last_name',
            'phone',
            'role',
        )

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        # Check for unique email and username
        if User.objects.filter(email=attrs.get('email')).exists():
            raise serializers.ValidationError({"email": "A user with that email already exists."})
        if User.objects.filter(username=attrs.get('username')).exists():
            raise serializers.ValidationError({"username": "A user with that username already exists."})
        if User.objects.filter(phone=attrs.get('phone')).exists():
            raise serializers.ValidationError({"phone": "A user with that phone already exists."})
        
        # Prevent admin and auditor roles from signing up
        if attrs.get('role') in ['ADMIN', 'AUDITOR']:  # Adjust as per your role constants
            raise serializers.ValidationError({"role": "Admin and Auditor roles cannot register."})
        
        return attrs

    def create(self, validated_data):
        # Remove password2 as it's not needed anymore
        validated_data.pop('password2', None)

        # Safely get optional fields with defaults
        first_name = validated_data.get('first_name', '')
        last_name = validated_data.get('last_name', '')
        phone = validated_data.get('phone', '')
        role = validated_data.get('role', 'USER')
        mfa_method = validated_data.get('mfa_method', 'email')
        mfa_enabled = validated_data.get('mfa_enabled', True)

        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=first_name,
            last_name=last_name,
            is_active=False,
            phone=phone,
            role=role,
            mfa_method=mfa_method,
            mfa_enabled=mfa_enabled
        )
        user.set_password(validated_data['password'])
        user.save()

        # Send activation email
        send_activation_email(user)

        return user


# Custom Token Serializer to include additional claims
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        username_or_email = attrs.get("username")  # Either email or username comes here
        password = attrs.get("password")

        # Access the request object through self.context
        request = self.context.get('request')
        if not request:
            raise serializers.ValidationError({"detail": "Request context is missing."})
        device_identifier = request.META.get('HTTP_USER_AGENT', '')

        user_obj = User.objects.filter(email=username_or_email).first() or User.objects.filter(username=username_or_email).first()
        
        if user_obj:
            if not user_obj.is_active:
                # If the user is inactive, resend activation email
                send_activation_email(user_obj)
                raise serializers.ValidationError({
                    "detail": "Your account is inactive. We've sent you a new activation email."
                })

            # Authenticate with the username, even if email was entered
            user = authenticate(username=user_obj.username, password=password)

            if user:
                # Check device information
                device_identifier = self.context['request'].META['HTTP_USER_AGENT']
                device_exists = UserDevice.objects.filter(user=user, device_identifier=device_identifier).exists()

                if user.mfa_enabled and not device_exists:
                    send_mfa_code(user)
                    return {'mfa_required': True, 'message': 'MFA code sent. Please verify.','user':user_obj}

                # Generate token for JWT login
                refresh = self.get_token(user)
                data = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'role': user.role,
                    'username': user.username,
                    'email': user.email,
                }
                # Record the device
                UserDevice.objects.update_or_create(
                    user=user,
                    device_identifier=device_identifier,
                    defaults={'last_login': timezone.now()}
                )

                return data
            else:
                raise serializers.ValidationError({"detail": "Invalid credentials."})
        else:
            raise serializers.ValidationError({"detail": "User not found."})


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'phone', 'role',  'mfa_method', 'mfa_enabled')