"""
API views for Academics app.
Provides tenant-isolated management of classes, sections, subjects, and sessions.
"""
from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.core.permissions import TenantContextMixin

from .models import AcademicClass, AcademicYear, Section, Subject
from .serializers import (
    AcademicClassSerializer,
    AcademicYearSerializer,
    SectionCreateSerializer,
    SectionSerializer,
    SubjectSerializer,
)


class AcademicClassListCreateView(TenantContextMixin, generics.ListCreateAPIView):
    """
    GET /api/v1/academics/classes/
    POST /api/v1/academics/classes/
    Lists or creates academic grade levels strictly scoped to the active tenant school.
    """
    serializer_class = AcademicClassSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        school = self.get_tenant_school()
        return (
            AcademicClass.objects.filter(school=school)
            .prefetch_related("sections")
            .order_by("order", "name")
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "status": "success",
            "data": serializer.data,
        })

    def perform_create(self, serializer):
        school = self.get_tenant_school()
        serializer.save(school=school)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {
                "status": "success",
                "message": f"Class '{serializer.data['name']}' created successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )


class SectionListCreateView(TenantContextMixin, generics.ListCreateAPIView):
    """
    GET /api/v1/academics/sections/
    POST /api/v1/academics/sections/
    Lists or creates sections scoped to the tenant school.
    """
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return SectionCreateSerializer
        return SectionSerializer

    def get_queryset(self):
        school = self.get_tenant_school()
        class_id = self.request.query_params.get("class_id")
        qs = Section.objects.filter(school=school)
        if class_id:
            qs = qs.filter(academic_class_id=class_id)
        return qs.order_by("academic_class__order", "name")

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "status": "success",
            "data": serializer.data,
        })

    def perform_create(self, serializer):
        school = self.get_tenant_school()
        academic_class = serializer.validated_data["academic_class"]
        if academic_class.school_id != school.id:
            raise PermissionDenied("Target class does not belong to your active school.")
        serializer.save(school=school)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {
                "status": "success",
                "message": f"Section '{serializer.data['name']}' created successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )


class SubjectListCreateView(TenantContextMixin, generics.ListCreateAPIView):
    """
    GET /api/v1/academics/subjects/
    POST /api/v1/academics/subjects/
    Lists or creates curriculum subjects for the tenant.
    """
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        school = self.get_tenant_school()
        return Subject.objects.filter(school=school).order_by("name")

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "status": "success",
            "data": serializer.data,
        })

    def perform_create(self, serializer):
        school = self.get_tenant_school()
        serializer.save(school=school)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {
                "status": "success",
                "message": f"Subject '{serializer.data['name']}' created successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )


class AcademicYearListView(TenantContextMixin, generics.ListAPIView):
    """
    GET /api/v1/academics/years/
    Lists academic years/sessions for the current tenant school.
    """
    serializer_class = AcademicYearSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        school = self.get_tenant_school()
        return AcademicYear.objects.filter(school=school).order_by("-is_current", "-start_date")

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "status": "success",
            "data": serializer.data,
        })
