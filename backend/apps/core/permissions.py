"""
Base tenant and role-based permissions for Darsentra ERP.
Enforces multi-tenant data isolation by verifying user memberships.
"""
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission


class TenantContextMixin:
    """
    Mixin for DRF views to automatically resolve and strictly validate
    the active school tenant from request headers or active memberships.
    """

    def get_tenant_school(self):
        from apps.schools.models import SchoolMembership
        from apps.schools.services import TenantSecurityService

        school_id = self.request.headers.get("X-School-ID")
        if school_id:
            return TenantSecurityService.validate_user_school_access(self.request.user, school_id)

        membership = SchoolMembership.objects.filter(
            user=self.request.user,
            is_active=True,
            school__is_active=True,
        ).select_related("school").first()

        if not membership:
            raise PermissionDenied("You must belong to an active school to access this resource.")
        return membership.school


class IsSchoolMember(BasePermission):
    """
    Ensures that the authenticated user has an active membership in the target school.
    Never trusts client-provided tenant IDs without validating membership.
    """
    message = "Access denied: You are not an active member of this school."

    def has_permission(self, request, view) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        school = getattr(view, "school", None)
        if callable(getattr(view, "get_school", None)):
            school = view.get_school()

        if school is None:
            return request.user.school_memberships.filter(is_active=True).exists()

        return request.user.school_memberships.filter(school=school, is_active=True).exists()

    def has_object_permission(self, request, view, obj) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

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
