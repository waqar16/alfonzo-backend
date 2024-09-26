from rest_framework.permissions import BasePermission


class IsAdminSuperUserOrAuditor(BasePermission):
    """
    Custom permission to grant access only to superusers, users with the ADMIN role,
    or users with the AUDITOR role (read-only access).
    """
    def has_permission(self, request, view):
        is_auditor = request.user.role == 'AUDITOR' and request.method in ['GET', 'HEAD', 'OPTIONS']
        is_admin_or_superuser = request.user and (request.user.is_superuser or request.user.role == 'ADMIN')
        return is_auditor or is_admin_or_superuser