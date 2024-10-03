from django.urls import path
from .views import LawyerProfileDetailUpdateView

urlpatterns = [
    path('lawyer-profile/', LawyerProfileDetailUpdateView.as_view(), name='profile_detail_update'),
]