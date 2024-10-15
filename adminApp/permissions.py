from rest_framework.permissions import BasePermission


class IsAdminSuperUserOrAuditor(BasePermission):
    """
    Custom permission to grant access only to superusers, users with the ADMIN role,
    or users with the AUDITOR role (read-only access).
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False
        
        # Check if user has ADMIN role or is a superuser
        is_admin_or_superuser = request.user.is_superuser or (getattr(request.user, 'role', None) == 'ADMIN')

        # Check if user is an AUDITOR with read-only access
        is_auditor = getattr(request.user, 'role', None) == 'AUDITOR' and request.method in ['GET', 'HEAD', 'OPTIONS']

        return is_auditor or is_admin_or_superuser
