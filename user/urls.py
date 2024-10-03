from django.urls import path
from .views import UserProfileDetailView, UserProfileCreateView


urlpatterns = [
    path('user-profile/create/', UserProfileCreateView.as_view(), name='user-profile-create'),
    path('user-profile/', UserProfileDetailView.as_view(), name='profile_detail_update'),
]
