"""
Service layer for Schools and Multi-Tenancy.
Implements business rules for tenant resolution, creation, and authorization.
"""
from django.db import transaction
from django.db.models import QuerySet
from django.utils.text import slugify
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
    Service managing school tenant creation, onboarding, and memberships.
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
    def setup_new_school(owner_user, data: dict) -> School:
        """
        Atomic school onboarding wizard processor:
        Creates the School tenant, attaches the owner membership,
        initializes the active academic session, and seeds the class/section hierarchy.
        """
        from apps.academics.models import AcademicClass, AcademicYear, Section

        name = data["name"].strip()
        code = data["code"].strip().upper()
        slug = slugify(f"{name}-{code}")

        school = School.objects.create(
            name=name,
            code=code,
            slug=slug,
            registration_number=data.get("registration_number", ""),
            curriculum_type=data.get("curriculum_type", "matric_fsc"),
            contact_email=data.get("contact_email", owner_user.email),
            phone_number=data.get("phone_number", getattr(owner_user, "phone_number", "")),
            address=data.get("address", ""),
            city=data.get("city", "Islamabad"),
            province=data.get("province", "islamabad"),
            is_active=True,
        )

        SchoolMembership.objects.create(
            user=owner_user,
            school=school,
            role=MembershipRole.OWNER,
            is_active=True,
        )

        # Create active Academic Year
        academic_year_name = data.get("academic_year_name", "2026-2027")
        AcademicYear.objects.create(
            school=school,
            name=academic_year_name,
            is_current=True,
        )

        # Seed initial classes and default Section A
        initial_classes = data.get("initial_classes", [])
        if not initial_classes:
            initial_classes = [
                "Nursery",
                "Prep",
                "Class 1",
                "Class 2",
                "Class 3",
                "Class 4",
                "Class 5",
                "Class 6",
                "Class 7",
                "Class 8",
                "Class 9",
                "Class 10",
            ]

        for idx, class_name in enumerate(initial_classes, start=1):
            cls_obj = AcademicClass.objects.create(
                school=school,
                name=class_name,
                order=idx,
            )
            Section.objects.create(
                school=school,
                academic_class=cls_obj,
                name="Section A",
                capacity=40,
            )

        return school
