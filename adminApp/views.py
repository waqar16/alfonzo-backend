from authentication.serializers import UserSerializer
from rest_framework import generics, status
from django.contrib.auth import get_user_model
from .permissions import IsAdminSuperUserOrAuditor
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from .models import Template, Category
from user.models import UserProfile
from lawyer.models import LawyerProfile
from .serializers import TemplateSerializer, CategorySerializer
from django.db.models import Q
from user.models import UserDocument
from lawyer.models import LawyerDocument
from .serializers import UserDocumentsListSerializer, LawyerDocumentsListSerializer
from rest_framework import viewsets

User = get_user_model()


class DocumentsViewSet(viewsets.ViewSet):
    permission_classes = [IsAdminSuperUserOrAuditor]

    def list(self, request):
        user_documents = UserDocument.objects.all()
        lawyer_documents = LawyerDocument.objects.all()

        user_documents_serialized = UserDocumentsListSerializer(user_documents, many=True).data
        lawyer_documents_serialized = LawyerDocumentsListSerializer(lawyer_documents, many=True).data

        return Response({
            'user_documents': user_documents_serialized,
            'lawyer_documents': lawyer_documents_serialized
        })


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminSuperUserOrAuditor]
    pagination_class = None

# class CategoryListView(generics.ListCreateAPIView):
#     """
#     GET /api/categories/
#     POST /api/categories/
#     List all categories and create a new category with subcategories.
#     """
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#     permission_classes = [IsAdminSuperUserOrAuditor]
#     pagination_class = None

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         try:
#             serializer.is_valid(raise_exception=True)
#             self.perform_create(serializer)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         except ValidationError as e:
#             return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class CategoryDetailView(generics.RetrieveAPIView):
#     """
#     GET /api/categories/<int:pk>/
#     Retrieve a specific category.
#     """
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#     permission_classes = [IsAdminSuperUserOrAuditor]
#     # permission_classes = [IsAuthenticated]


# List all users (admin only)
class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdminSuperUserOrAuditor]

    def get_queryset(self):
        # Get role from query params
        role = self.request.query_params.get('role', None)

        # Base queryset for all users ordered by the date they joined
        queryset = User.objects.all().order_by('-date_joined')

        # Filter users by role if a role is specified in the query params
        if role:
            queryset = queryset.filter(Q(role__iexact=role))

        return queryset


# Retrieve and update a specific user (admin only)
class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminSuperUserOrAuditor]


# Delete a specific user (admin only)
class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminSuperUserOrAuditor]


# List and create templates (admin only)
class TemplateListCreateView(generics.ListCreateAPIView):
    """
    API view to list and create templates.
    """
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer
    pagination_class = None

    def get_queryset(self):
        queryset = super().get_queryset()
   
        # Get query parameters
        category_name = self.request.query_params.get('category', None)
        sub_category_name = self.request.query_params.get('sub_category', None)

        # Filter based on category name
        if category_name:
            queryset = queryset.filter(category__name__icontains=category_name)

        # Filter based on sub-category name
        if sub_category_name:
            queryset = queryset.filter(SubCategory__name__icontains=sub_category_name)

        return queryset

    # Define custom permission classes
    def get_permissions(self):
        if self.request.method == 'POST':
            # Only admins can create templates
            self.permission_classes = [IsAdminSuperUserOrAuditor]
        else:
            # Allow any user to list templates
            self.permission_classes = [IsAuthenticated]

        return super().get_permissions()

    # def get(self, request, *args, **kwargs):
    #     """
    #     Get a list of all templates.
    #     """
    #     templates = self.get_queryset()
    #     serializer = self.get_serializer(templates, many=True)
    #     return Response(serializer.data)

    # def post(self, request, *args, **kwargs):
    #     """
    #     Create a new template.
    #     """
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     template = serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)


class TemplateDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update or delete a template.
    """
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer

    # Allow authenticated users for all methods
    permission_classes = [IsAuthenticated]  # Adjust permissions as needed

    def get(self, request, *args, **kwargs):
        """
        Retrieve a specific template.
        """
        template = self.get_object()
        serializer = self.get_serializer(template)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        """
        Update a specific template.
        """
        template = self.get_object()
        serializer = self.get_serializer(template, data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_template = serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        """
        Delete a specific template.
        """
        template = self.get_object()
        template.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserActivityOverview(APIView):
    permission_classes = [IsAdminSuperUserOrAuditor]

    def get(self, request):
        total_users = User.objects.count()
        active_users = User.objects.filter(is_active=True).count()
        inactive_users = total_users - active_users
        
        data = {
            'total_users': total_users,
            'active_users': active_users,
            'inactive_users': inactive_users,
        }
        
        return Response(data)


class MFAUsageStatistics(APIView):
    permission_classes = [IsAdminSuperUserOrAuditor]

    def get(self, request):
        total_users = User.objects.count()
        users_with_mfa = User.objects.filter(mfa_enabled=True).count()
        
        data = {
            'total_users': total_users,
            'users_with_mfa': users_with_mfa,
            'mfa_percentage': (users_with_mfa / total_users * 100) if total_users else 0,
        }
        
        return Response(data)


class RoleDistribution(APIView):
    permission_classes = [IsAdminSuperUserOrAuditor]

    def get(self, request):
        role_distribution = User.objects.values('role').annotate(count=Count('role'))
        
        data = {
            'role_distribution': list(role_distribution),
        }
        
        return Response(data)


class TemplateOverview(APIView):
    permission_classes = [IsAdminSuperUserOrAuditor]

    def get(self, request):
        total_templates = Template.objects.count()
        templates_by_category = Template.objects.values('category').annotate(count=Count('id'))

        data = {
            'total_templates': total_templates,
            'templates_by_category': list(templates_by_category),
        }
        
        return Response(data)


class MostUsedTemplatesByUser(APIView):
    permission_classes = [IsAdminSuperUserOrAuditor]

    def get(self, request):
        # Count how many users have each template
        most_used_templates = UserProfile.objects.values('template__name').annotate(user_count=Count('id')).order_by('-user_count')

        data = {
            'most_used_templates': list(most_used_templates),
        }

        return Response(data)


class MostUsedTemplatesByLawyer(APIView):
    permission_classes = [IsAdminSuperUserOrAuditor]

    def get(self, request):
        # Count how many users have each template
        most_used_templates = LawyerProfile.objects.values('template__name').annotate(user_count=Count('id')).order_by('-user_count')

        data = {
            'most_used_templates': list(most_used_templates),
        }

        return Response(data)
