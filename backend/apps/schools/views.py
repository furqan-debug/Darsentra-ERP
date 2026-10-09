"""
API Views for Schools and Memberships.
Enforces multi-tenant data isolation by scoping all queries to the requesting user's verified schools.
"""
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import SchoolMembership
from .permissions import IsSchoolMember
from .serializers import SchoolMembershipSerializer, SchoolSerializer
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
        # Validate membership through security service
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
