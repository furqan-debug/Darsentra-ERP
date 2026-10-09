"""
Service layer for Schools and Multi-Tenancy.
Implements business rules for tenant resolution, creation, and authorization.
"""
from django.db import transaction
from django.db.models import QuerySet
from rest_framework.exceptions import PermissionDenied

from .models import MembershipRole, School, SchoolMembership


class TenantSecurityService:
    """
    Central service enforcing multi-tenant isolation.
    Guarantees that a user only ever interacts with data belonging to schools
    they possess active membership in.
    """

    @staticmethod
    def validate_user_school_access(user, school_id_or_instance) -> School:
        """
        Validates that the user has an active membership for the given school.
        Raises PermissionDenied if access is not permitted.
        Never trusts client-provided school IDs.
        """
        if not user or not user.is_authenticated:
            raise PermissionDenied("Authentication required to access tenant data.")

        if user.is_superuser:
            if isinstance(school_id_or_instance, School):
                return school_id_or_instance
            school = School.objects.filter(id=school_id_or_instance, is_active=True).first()
            if not school:
                raise PermissionDenied("Requested school does not exist or is inactive.")
            return school

        if isinstance(school_id_or_instance, School):
            school_id = school_id_or_instance.id
        else:
            school_id = school_id_or_instance

        membership = SchoolMembership.objects.filter(
            user=user,
            school_id=school_id,
            is_active=True,
            school__is_active=True,
        ).select_related("school").first()

        if not membership:
            raise PermissionDenied("Access denied: You do not have an active membership in this school.")

        return membership.school


class SchoolService:
    """
    Service managing school tenant creation and memberships.
    """

    @staticmethod
    def get_user_schools(user) -> QuerySet[School]:
        """
        Retrieves all active schools where the user has an active membership.
        Superusers can access all active schools.
        """
        if not user or not user.is_authenticated:
            return School.objects.none()

        if user.is_superuser:
            return School.objects.filter(is_active=True)

        return School.objects.filter(
            memberships__user=user,
            memberships__is_active=True,
            is_active=True,
        ).distinct()

    @staticmethod
    @transaction.atomic
    def create_school_with_owner(
        name: str,
        code: str,
        slug: str,
        owner_user,
        **extra_fields,
    ) -> School:
        """
        Creates a new school tenant and assigns the creator as OWNER.
        """
        school = School.objects.create(
            name=name,
            code=code,
            slug=slug,
            **extra_fields,
        )
        SchoolMembership.objects.create(
            user=owner_user,
            school=school,
            role=MembershipRole.OWNER,
            is_active=True,
        )
        return school
