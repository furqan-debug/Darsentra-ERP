"""
Base tenant and role-based permissions for Darsentra ERP.
Enforces multi-tenant data isolation by verifying user memberships.
"""
from rest_framework.permissions import BasePermission


class IsSchoolMember(BasePermission):
    """
    Ensures that the authenticated user has an active membership in the target school.
    Never trusts client-provided tenant IDs without validating membership.
    """
    message = "Access denied: You are not an active member of this school."

    def has_permission(self, request, view) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False

        # Superusers have system-wide administrative access
        if request.user.is_superuser:
            return True

        # Check if view provides get_school() or has school attribute
        school = getattr(view, "school", None)
        if callable(getattr(view, "get_school", None)):
            school = view.get_school()

        if school is None:
            # If view doesn't explicitly bind to a single school,
            # ensure user has at least one active school membership
            return request.user.school_memberships.filter(is_active=True).exists()

        return request.user.school_memberships.filter(school=school, is_active=True).exists()

    def has_object_permission(self, request, view, obj) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        # Determine target school from the object
        target_school = getattr(obj, "school", obj if hasattr(obj, "memberships") else None)
        if target_school is None:
            return False

        return request.user.school_memberships.filter(school=target_school, is_active=True).exists()


class IsSchoolAdmin(BasePermission):
    """
    Ensures the user has an administrative role (OWNER, PRINCIPAL, or ADMIN) in the school.
    """
    message = "Access denied: Administrative privileges required for this school."
    ADMIN_ROLES = ["owner", "principal", "admin"]

    def has_permission(self, request, view) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        school = getattr(view, "school", None)
        if callable(getattr(view, "get_school", None)):
            school = view.get_school()

        if school is None:
            return request.user.school_memberships.filter(
                role__in=self.ADMIN_ROLES, is_active=True
            ).exists()

        return request.user.school_memberships.filter(
            school=school, role__in=self.ADMIN_ROLES, is_active=True
        ).exists()
