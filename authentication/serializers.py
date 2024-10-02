from django.utils import timezone
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from .utils import send_activation_email, send_mfa_code
from user.models import UserDevice

User = get_user_model()


# User Registration Serializer
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'phone', 'mfa_method', 'mfa_enabled', 'first_name', 'last_name')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        # Check for unique email and username
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "A user with that email already exists."})
        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError({"username": "A user with that username already exists."})
        
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            is_active=False,
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
            # Authenticate with the username, even if email was entered
            user = authenticate(username=user_obj.username, password=password)

            if user:
                if not user.is_active:
                    # If the user is inactive, resend activation email
                    send_activation_email(user)
                    raise serializers.ValidationError({
                        "detail": "Your account is inactive. We've sent you a new activation email."
                    })
        
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
        fields = ('first_name', 'last_name', 'username', 'email', 'phone', 'mfa_method', 'mfa_enabled')