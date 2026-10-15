"""
Views for Accounts app.
Provides JWT authentication, self-service registration, and user profile management.
"""
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.schools.models import SchoolMembership

from .serializers import (
    CustomTokenObtainPairSerializer,
    UserRegistrationSerializer,
    UserSummarySerializer,
)


class LoginView(TokenObtainPairView):
    """
    POST /api/v1/accounts/token/
    Authenticates a user by email and password, returning JWT tokens,
    user details, and all active school memberships.
    """
    serializer_class = CustomTokenObtainPairSerializer


class RegisterView(APIView):
    """
    POST /api/v1/accounts/register/
    Self-service registration for school founders and administrators.
    Automatically generates JWT tokens upon successful sign-up.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "status": "success",
                    "message": "Account created successfully.",
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "user": UserSummarySerializer(user).data,
                    "schools": [],
                    "active_school": None,
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


class CurrentUserView(APIView):
    """
    GET /api/v1/accounts/me/
    Returns the authenticated user's profile and active school tenant memberships.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        memberships = SchoolMembership.objects.filter(
            user=user,
            is_active=True,
            school__is_active=True,
        ).select_related("school")

        schools_data = [
            {
                "id": str(m.school.id),
                "name": m.school.name,
                "code": m.school.code,
                "slug": m.school.slug,
                "curriculum_type": m.school.curriculum_type,
                "curriculum_display": m.school.get_curriculum_type_display(),
                "city": m.school.city,
                "province": m.school.province,
                "role": m.role,
                "role_display": m.get_role_display(),
            }
            for m in memberships
        ]

        active_school = schools_data[0] if len(schools_data) > 0 else None

        return Response(
            {
                "status": "success",
                "data": {
                    "user": UserSummarySerializer(user).data,
                    "schools": schools_data,
                    "active_school": active_school,
                },
            }
        )
