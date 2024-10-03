from django.urls import path
from .views import UserProfileDetailUpdateView

urlpatterns = [
    path('profile/', UserProfileDetailUpdateView.as_view(), name='profile_detail_update'),
]