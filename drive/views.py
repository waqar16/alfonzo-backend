import os
import io
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from django.core.mail import EmailMessage
import base64


class UploadPDFView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Check if a file is provided in the request
        if 'file' not in request.FILES:
            return Response({'error': 'No file provided. Please upload a PDF file.'}, status=status.HTTP_400_BAD_REQUEST)

        file = request.FILES['file']

        # Check if the uploaded file is a PDF
        if not file.name.endswith('.pdf'):
            return Response({'error': 'Uploaded file is not a PDF. Please upload a valid PDF file.'}, status=status.HTTP_400_BAD_REQUEST)

        # Update this path to the actual location of your credentials.json file
        creds_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'credentials.json')

        # Authenticate with Google Drive API
        creds = service_account.Credentials.from_service_account_file(
            creds_path,
            scopes=['https://www.googleapis.com/auth/drive.file']
        )

        drive_service = build('drive', 'v3', credentials=creds)

        file_metadata = {
            'name': file.name,
            'mimeType': 'application/pdf'
        }

        # Use BytesIO to read the file into memory
        file_stream = io.BytesIO(file.read())

        # Create a MediaIoBaseUpload object for the in-memory file
        media = MediaIoBaseUpload(file_stream, mimetype='application/pdf')

        # Upload file to Google Drive
        try:
            uploaded_file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            file_id = uploaded_file.get('id')

            # Make the file publicly accessible
            drive_service.permissions().create(
                fileId=file_id,
                body={'role': 'reader', 'type': 'anyone'},
            ).execute()

            # Generate the file URL
            file_url = f"https://drive.google.com/file/d/{file_id}/view?usp=sharing"
            return Response({'file_url': file_url}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SendEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            # Extract data from the request body
            email = request.data.get('email')
            subject = request.data.get('subject')
            message = request.data.get('message')
            pdf_file = request.data.get('pdf_file')

            if not email:
                return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
            if not subject:
                return Response({'error': 'Subject is required'}, status=status.HTTP_400_BAD_REQUEST)
            if not message:
                return Response({'error': 'Message is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Define the subject
            subject = f"LegalEase: {subject}"

            message = f"""
            <html>
                <body>
                    <p>{message}</p>
                </body>
            </html>
            """

            # Create email message with HTML content
            email_message = EmailMessage(
                subject=subject,
                body=message,
                to=[email],
            )
            
            # Attach the PDF to the email
            email_message.attach_file(pdf_file)

            # Specify that the email contains HTML content
            email_message.content_subtype = 'html'

            # Send the email
            email_message.send()

            return Response({'message': 'Email sent successfully.'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)