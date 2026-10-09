"""Permissions for Examinations app."""
from apps.core.permissions import IsSchoolAdmin, IsSchoolMember

__all__ = ["IsSchoolMember", "IsSchoolAdmin"]
