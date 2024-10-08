from django.urls import path
from .views import LawyerProfileDetailUpdateView, LawyerProfileCreateView, LawyerProfileListView

urlpatterns = [
    path('lawyer-profile/create/', LawyerProfileCreateView.as_view(), name='user-profile-create'),
    path('lawyer-profile/<int:pk>/', LawyerProfileDetailUpdateView.as_view(), name='profile_detail_update'),
    path('lawyer-profiles/', LawyerProfileListView.as_view(), name='lawyer-profile-list-create'),
]
