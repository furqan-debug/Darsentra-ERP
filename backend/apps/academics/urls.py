"""
URL configuration for Academics app.
"""
from django.urls import path

from .views import (
    AcademicClassListCreateView,
    AcademicYearListView,
    SectionListCreateView,
    SubjectListCreateView,
)

app_name = "academics"

urlpatterns = [
    path("classes/", AcademicClassListCreateView.as_view(), name="class-list-create"),
    path("sections/", SectionListCreateView.as_view(), name="section-list-create"),
    path("subjects/", SubjectListCreateView.as_view(), name="subject-list-create"),
    path("years/", AcademicYearListView.as_view(), name="year-list"),
]
