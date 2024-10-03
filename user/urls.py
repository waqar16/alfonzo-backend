from django.urls import path
from .views import UserProfileDetailView


urlpatterns = [
    path('user-profile/', UserProfileDetailView.as_view(), name='profile_detail_update'),
]
