"""Permissions for Attendance app."""
from apps.core.permissions import IsSchoolAdmin, IsSchoolMember

__all__ = ["IsSchoolMember", "IsSchoolAdmin"]
