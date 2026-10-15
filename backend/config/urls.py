"""
Root URL Configuration for Darsentra ERP.
All API endpoints are namespaced under /api/v1/.
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # Core system endpoints (health check)
    path("api/v1/", include("apps.core.urls", namespace="core")),
    # Domain modules
    path("api/v1/accounts/", include("apps.accounts.urls", namespace="accounts")),
    path("api/v1/schools/", include("apps.schools.urls", namespace="schools")),
    path("api/v1/academics/", include("apps.academics.urls", namespace="academics")),
    path("api/v1/students/", include("apps.students.urls", namespace="students")),
    path("api/v1/attendance/", include("apps.attendance.urls", namespace="attendance")),
    path("api/v1/examinations/", include("apps.examinations.urls", namespace="examinations")),
    path("api/v1/fees/", include("apps.fees.urls", namespace="fees")),
    path("api/v1/staff/", include("apps.staff.urls", namespace="staff")),
    path("api/v1/reports/", include("apps.reports.urls", namespace="reports")),
]
