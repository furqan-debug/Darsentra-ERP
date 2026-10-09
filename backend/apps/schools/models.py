"""
Foundational multi-tenant models for Darsentra ERP: School and SchoolMembership.
"""
import uuid

from django.conf import settings
from django.db import models

from apps.core.models import TimeStampedModel


class CurriculumType(models.TextChoices):
    MATRIC_FSC = "matric_fsc", "Matric / FSc (BISE)"
    CAMBRIDGE = "cambridge", "Cambridge (O/A Levels)"
    FEDERAL_BOARD = "federal_board", "Federal Board (FBISE)"
    IB = "ib", "International Baccalaureate"
    COMBINED = "combined", "Combined / Multiple Streams"


class ProvinceChoices(models.TextChoices):
    ISLAMABAD = "islamabad", "Islamabad Capital Territory"
    PUNJAB = "punjab", "Punjab"
    SINDH = "sindh", "Sindh"
    KPK = "kpk", "Khyber Pakhtunkhwa"
    BALOCHISTAN = "balochistan", "Balochistan"
    AJK = "ajk", "Azad Jammu and Kashmir"
    GILGIT_BALTISTAN = "gilgit_baltistan", "Gilgit-Baltistan"


class MembershipRole(models.TextChoices):
    OWNER = "owner", "School Owner / Board Trustee"
    PRINCIPAL = "principal", "Principal / Headmaster"
    ADMIN = "admin", "School Administrator"
    TEACHER = "teacher", "Teacher / Faculty"
    ACCOUNTANT = "accountant", "Accountant / Bursar"
    STUDENT = "student", "Student"
    PARENT = "parent", "Parent / Guardian"
    STAFF = "staff", "Support Staff"


class School(TimeStampedModel):
    """
    Primary Tenant entity in Darsentra ERP.
    Represents an independent educational institution or campus.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=100, unique=True, db_index=True)
    code = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
        help_text="Institutional identifier (e.g. BSS-ISB-01)",
    )
    registration_number = models.CharField(
        max_length=100,
        blank=True,
        help_text="Government / Regulatory Registration Number (e.g., PEIRA/BISE)",
    )
    curriculum_type = models.CharField(
        max_length=50,
        choices=CurriculumType.choices,
        default=CurriculumType.MATRIC_FSC,
    )
    contact_email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=30, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, default="Islamabad")
    province = models.CharField(
        max_length=50,
        choices=ProvinceChoices.choices,
        default=ProvinceChoices.ISLAMABAD,
    )
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Suspended schools cannot be accessed by their users.",
    )

    class Meta:
        verbose_name = "School"
        verbose_name_plural = "Schools"
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.code})"


class SchoolMembership(TimeStampedModel):
    """
    Associates an authenticated User with a School tenant and defines their role.
    This forms the backbone of Darsentra ERP's multi-tenant isolation and RBAC.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="school_memberships",
    )
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    role = models.CharField(
        max_length=30,
        choices=MembershipRole.choices,
        default=MembershipRole.TEACHER,
    )
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Inactive memberships cannot access school tenant data.",
    )

    class Meta:
        verbose_name = "School Membership"
        verbose_name_plural = "School Memberships"
        unique_together = ("user", "school")
        ordering = ["school", "role"]

    def __str__(self) -> str:
        return f"{self.user} - {self.school.name} ({self.get_role_display()})"
