from django.urls import path
from .views import FeedbackListCreateView, FeedbackDetailView, TopFeedbacksView

urlpatterns = [
    path('feedback/', FeedbackListCreateView.as_view(), name='feedback-list-create'),  # For listing and creating feedback
    path('feedback/<int:pk>/', FeedbackDetailView.as_view(), name='feedback-detail'),  # For retrieving, updating, and deleting feedback
    path('top-feedbacks/', TopFeedbacksView.as_view(), name='top-feedbacks'),
]
