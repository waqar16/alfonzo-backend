from django.contrib import admin
from .models import LawyerProfile, LawyerDocument, UserQuery

admin.site.register(LawyerProfile)
admin.site.register(LawyerDocument)
admin.site.register(UserQuery)
