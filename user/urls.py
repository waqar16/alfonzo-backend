from django.urls import path
from .views import (
    UserProfileCreateView,
    UserProfileDetailView,
    UserDocumentListCreateAPIView,
    UserDocumentDetailAPIView,
    LawyerUpdateVerificationAPIView
)


urlpatterns = [
    path('user-profile/create/', UserProfileCreateView.as_view(), name='user-profile-create'),
    path('user-profile/', UserProfileDetailView.as_view(), name='profile_detail_update'),
    path('documents/', UserDocumentListCreateAPIView.as_view(), name='user-document-list-create'),
    path('documents/<int:pk>/', UserDocumentDetailAPIView.as_view(), name='user-document-detail'),
    path('user-documents/<int:pk>/update-verification/', LawyerUpdateVerificationAPIView.as_view(), name='update-verification'),
]
