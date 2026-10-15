"""
API Views for Schools and Memberships.
Enforces multi-tenant data isolation by scoping all queries to the requesting user's verified schools.
"""
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.academics.models import AcademicClass, AcademicYear, Section

from .models import SchoolMembership
from .permissions import IsSchoolMember
from .serializers import SchoolMembershipSerializer, SchoolSerializer, SchoolSetupSerializer
from .services import SchoolService, TenantSecurityService


class UserSchoolsListView(generics.ListAPIView):
    """
    Lists only the schools where the authenticated user holds an active membership.
    Prevents discovery of other tenants.
    """
    serializer_class = SchoolSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SchoolService.get_user_schools(self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "status": "success",
            "data": serializer.data,
        })


class SchoolDetailView(APIView):
    """
    Retrieves details for a specific school.
    Strictly verifies that the user is an active member. Never trusts client ID blindly.
    """
    permission_classes = [IsAuthenticated, IsSchoolMember]

    def get(self, request, school_id):
        school = TenantSecurityService.validate_user_school_access(request.user, school_id)
        serializer = SchoolSerializer(school)
        return Response({
            "status": "success",
            "data": serializer.data,
        })


class UserMembershipsListView(generics.ListAPIView):
    """
    Lists the authenticated user's active school memberships and roles.
    """
    serializer_class = SchoolMembershipSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            SchoolMembership.objects.filter(
                user=self.request.user,
                is_active=True,
                school__is_active=True,
            )
            .select_related("school")
            .order_by("school__name")
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "status": "success",
            "data": serializer.data,
        })


class SchoolSetupView(APIView):
    """
    POST /api/v1/schools/setup/
    Onboarding endpoint for school founders to initialize a new school tenant,
    set up active academic session, and generate initial grade levels.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SchoolSetupSerializer(data=request.data)
        if serializer.is_valid():
            school = SchoolService.setup_new_school(request.user, serializer.validated_data)
            return Response(
                {
                    "status": "success",
                    "message": f"School '{school.name}' has been successfully set up.",
                    "data": SchoolSerializer(school).data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {
                "status": "error",
                "code": "validation_error",
                "message": "Please correct the errors in the form.",
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class ActiveSchoolView(APIView):
    """
    GET /api/v1/schools/active/
    Returns detailed metrics and status of the current tenant school context
    (resolved via X-School-ID header or defaulting to user's primary school).
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        school_id = request.headers.get("X-School-ID")
        user = request.user

        membership = None
        if school_id:
            try:
                membership = SchoolMembership.objects.filter(
                    user=user,
                    school_id=school_id,
                    is_active=True,
                    school__is_active=True,
                ).select_related("school").first()
            except Exception:
                membership = None

        if not membership:
            # Fall back to user's first active membership
            membership = SchoolMembership.objects.filter(
                user=user,
                is_active=True,
                school__is_active=True,
            ).select_related("school").first()

        if not membership:
            return Response(
                {
                    "status": "success",
                    "data": {
                        "has_school": False,
                        "school": None,
                        "stats": None,
                    },
                }
            )

        school = membership.school
        current_session = AcademicYear.objects.filter(school=school, is_current=True).first()
        total_classes = AcademicClass.objects.filter(school=school).count()
        total_sections = Section.objects.filter(school=school).count()

        return Response(
            {
                "status": "success",
                "data": {
                    "has_school": True,
                    "school": SchoolSerializer(school).data,
                    "role": membership.role,
                    "role_display": membership.get_role_display(),
                    "stats": {
                        "total_students": 0,
                        "total_staff": 1,
                        "total_classes": total_classes,
                        "total_sections": total_sections,
                        "active_session": current_session.name if current_session else "N/A",
                    },
                },
            }
        )
