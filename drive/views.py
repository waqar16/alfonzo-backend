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
            pdf_data_url = request.data.get('pdf')

            if not email or not pdf_data_url:
                return Response({'error': 'Email and PDF data are required.'}, status=status.HTTP_400_BAD_REQUEST)

            # Decode Base64 PDF content
            pdf_base64 = pdf_data_url.split(',')[1]
            pdf_bytes = base64.b64decode(pdf_base64)
            pdf_filename = 'document.pdf'

            # Define the subject
            subject = "Your Document from LegalEase"

            message = f"""
            <html>
            <body style="font-family: Arial, sans-serif; color: #333; background-color: #f9f9f9; padding: 20px;">
                <div style="max-width: 600px; margin: 0 auto; background-color: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
                    <h2 style="text-align: center; color: #4CAF50;">LegalEase</h2>
                    <p>Dear User,</p>
                    <p>We hope this message finds you well. Attached to this email is your document, created and verified through LegalEase. You can download it for your records or use it as necessary.</p>
                    <p>Here are your document details:</p>
                    <ul style="line-height: 1.6;">
                        <li><strong>Title:</strong> LegalEase Document</li>
                    </ul>
                    <p>If you have any questions, feel free to reply to this email or contact our support team.</p>
                    <p>Thank you for using LegalEase!</p>
                    <p style="text-align: center; color: #999;">&copy; {2024} LegalEase, All rights reserved.</p>
                </div>
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
            email_message.attach(pdf_filename, pdf_bytes, 'application/pdf')

            # Specify that the email contains HTML content
            email_message.content_subtype = 'html'

            # Send the email
            email_message.send()

            return Response({'message': 'Email sent successfully.'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)