from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView,
    MyTokenObtainPairView,
    ActivateAccountView,
    GoogleLoginAPIView,
    LinkedInCallbackView,
    LinkedInLoginRedirect,
    ResetPasswordView,
    ResetPasswordLinkView,
    DeactivateAccountView,
    MFASettingsView,
    VerifyMFAView,
    LoggedInUserView,
    LogoutView,
    ChangeUsernameView,
    AuthGuardView
)

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='register'),
    path('login/', MyTokenObtainPairView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/me/', LoggedInUserView.as_view(), name='logged-in-user'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('activate/<uidb64>/<token>/', ActivateAccountView.as_view(), name='activate'),
    path('google/', GoogleLoginAPIView.as_view(), name="google-login"),
    path('linkedin/login/', LinkedInLoginRedirect.as_view(), name='linkedin-login'),
    path('linkedin/callback/', LinkedInCallbackView.as_view(), name='linkedin-callback'),
    path('reset-password/', ResetPasswordView.as_view(), name='password_reset_complete'),
    path('reset-password-link/', ResetPasswordLinkView.as_view(), name='reset-password-link'),
    path('deactivate-account/', DeactivateAccountView.as_view(), name='deactivate-account'),
    path('mfa-settings/', MFASettingsView.as_view(), name='mfa_settings'),
    path('verify-mfa/', VerifyMFAView.as_view(), name='verify_mfa'),
    path('change-username/', ChangeUsernameView.as_view(), name='change_username'),
    path('auth-guard/', AuthGuardView.as_view(), name='auth_guard'),
]
