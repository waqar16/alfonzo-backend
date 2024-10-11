from django.urls import path
from .views import UploadPDFView, SendEmailView

urlpatterns = [
    path('upload-pdf/', UploadPDFView.as_view(), name='upload_pdf'),
    path('send-document-email/', SendEmailView.as_view(), name='send-email'),
]
