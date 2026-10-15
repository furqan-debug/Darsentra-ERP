"""
Academic hierarchy models for Darsentra ERP.
Defines Academic Years, Classes, Sections, and Subjects strictly scoped by School tenant.
"""
from django.db import models

from apps.core.models import TenantScopedModel


class AcademicYear(TenantScopedModel):
    """
    Represents an annual academic session within a school (e.g., '2026-2027').
    """
    name = models.CharField(max_length=50, help_text="e.g. 2026-2027")
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=True, help_text="Designates the active session.")

    class Meta(TenantScopedModel.Meta):
        verbose_name = "Academic Year"
        verbose_name_plural = "Academic Years"
        unique_together = ("school", "name")
        ordering = ["-start_date", "-created_at"]

    def __str__(self) -> str:
        return f"{self.school.name} - {self.name}"


class AcademicClass(TenantScopedModel):
    """
    Represents a grade or educational level within a school (e.g., 'Class 9', 'Grade 10', 'O-Levels Year 1').
    """
    name = models.CharField(max_length=100, help_text="e.g. Nursery, Class 1, Grade 9, O-1")
    code = models.CharField(max_length=30, blank=True, help_text="Optional short code e.g. C-09")
    order = models.PositiveIntegerField(default=1, help_text="Ordinal sorting rank for display.")

    class Meta(TenantScopedModel.Meta):
        verbose_name = "Academic Class"
        verbose_name_plural = "Academic Classes"
        unique_together = ("school", "name")
        ordering = ["order", "name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.school.code})"


class Section(TenantScopedModel):
    """
    Represents a student cohort/classroom division within an AcademicClass (e.g. 'Section A', 'Rose').
    """
    academic_class = models.ForeignKey(
        AcademicClass,
        on_delete=models.CASCADE,
        related_name="sections",
    )
    name = models.CharField(max_length=50, default="Section A", help_text="e.g. Section A, Rose, Jasmine")
    room_number = models.CharField(max_length=30, blank=True)
    capacity = models.PositiveIntegerField(default=40)

    class Meta(TenantScopedModel.Meta):
        verbose_name = "Section"
        verbose_name_plural = "Sections"
        unique_together = ("academic_class", "name")
        ordering = ["academic_class", "name"]

    def __str__(self) -> str:
        return f"{self.academic_class.name} - {self.name}"


class Subject(TenantScopedModel):
    """
    Represents a taught subject within a school curriculum.
    """
    name = models.CharField(max_length=100, help_text="e.g. Mathematics, Physics, Urdu, Islamiyat")
    code = models.CharField(max_length=30, blank=True, help_text="e.g. MATH-09")
    is_elective = models.BooleanField(default=False)

    class Meta(TenantScopedModel.Meta):
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"
        unique_together = ("school", "name")
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.school.code})"


class ClassSubject(TenantScopedModel):
    """
    Maps a curriculum Subject to an AcademicClass with assigned weekly periods.
    """
    academic_class = models.ForeignKey(
        AcademicClass,
        on_delete=models.CASCADE,
        related_name="class_subjects",
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="assigned_classes",
    )
    weekly_periods = models.PositiveIntegerField(default=5)

    class Meta(TenantScopedModel.Meta):
        verbose_name = "Class Subject"
        verbose_name_plural = "Class Subjects"
        unique_together = ("academic_class", "subject")

    def __str__(self) -> str:
        return f"{self.academic_class.name} - {self.subject.name}"
