from django.urls import path
from .views import LawyerProfileDetailUpdateView, LawyerProfileCreateView

urlpatterns = [
    path('lawyer-profile/create/', LawyerProfileCreateView.as_view(), name='user-profile-create'),
    path('lawyer-profile/', LawyerProfileDetailUpdateView.as_view(), name='profile_detail_update'),
]