from django.urls import path
from .views import (
    UserProfileCreateView,
    UserProfileDetailView,
    UserDocumentCreateView,
    UserDocumentRetrieveUpdateDestroyView
)


urlpatterns = [
    path('user-profile/create/', UserProfileCreateView.as_view(), name='user-profile-create'),
    path('user-profile/', UserProfileDetailView.as_view(), name='profile_detail_update'),
    path('documents/', UserDocumentCreateView.as_view(), name='user-document-list-create'),
    path('documents/<int:pk>/', UserDocumentRetrieveUpdateDestroyView.as_view(), name='user-document-detail'),
]
