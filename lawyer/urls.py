from django.urls import path
from .views import (
    LawyerProfileCreateView,
    LawyerProfileDetailUpdateView,
    LawyerProfileListView,
    SendQueryToLawyerAPIView,
    LawyerUpdateVerificationAPIView,
    CombinedDocumentsListAPIView,
    LawyerDocumentListCreateAPIView,
    LawyerDocumentDetailAPIView
)

urlpatterns = [
    path('lawyer-profile/create/', LawyerProfileCreateView.as_view(), name='user-profile-create'),
    path('lawyer-profile/', LawyerProfileDetailUpdateView.as_view(), name='profile_detail_update'),
    path('lawyer-profiles/', LawyerProfileListView.as_view(), name='lawyer-profile-list-create'),
    path('lawyer/documents/', LawyerDocumentListCreateAPIView.as_view(), name='lawyer-document-list-create'),
    path('lawyer/documents/<int:pk>/', LawyerDocumentDetailAPIView.as_view(), name='lawyer-document-detail'),
    path('queries/send/', SendQueryToLawyerAPIView.as_view(), name='send-query'),
    path('lawyer-documents/<int:pk>/update-verification/', LawyerUpdateVerificationAPIView.as_view(), name='update-verification'),
    path('documents-for-lawyer/', CombinedDocumentsListAPIView.as_view(), name='combined-documents'),
]
