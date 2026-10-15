"""
Permissions for Accounts app.
"""
from rest_framework.permissions import BasePermission


class IsAccountOwner(BasePermission):
    """
    Allows access only to the user themselves.
    """
    def has_object_permission(self, request, view, obj) -> bool:
        return bool(request.user and request.user.is_authenticated and obj == request.user)
