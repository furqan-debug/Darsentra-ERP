"""
Shared base models for Darsentra ERP.
Provides abstract models for timestamps and tenant-scoped domain entities.
"""
from django.db import models


class TimeStampedModel(models.Model):
    """
    Abstract base model providing self-updating created_at and updated_at fields.
    """
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]


class TenantScopedModel(TimeStampedModel):
    """
    Abstract base model for all tenant-scoped data in Darsentra ERP.
    Every school-specific record MUST inherit from this model to ensure
    it is strictly bound to a single school tenant.
    """
    school = models.ForeignKey(
        "schools.School",
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_records",
        db_index=True,
        help_text="Tenant reference to which this record belongs.",
    )

    class Meta:
        abstract = True
        ordering = ["-created_at"]
