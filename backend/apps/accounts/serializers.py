"""
Serializers for Accounts app.
Includes JWT token generation with school membership metadata and user registration.
"""
from typing import Any

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.schools.models import SchoolMembership

from .models import User


class UserSummarySerializer(serializers.ModelSerializer):
    """
    Lightweight user profile serializer for authenticated context.
    """
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "phone_number",
            "cnic",
            "is_staff",
            "is_superuser",
            "is_active",
            "date_joined",
        ]
        read_only_fields = ["id", "email", "date_joined", "is_active", "is_staff", "is_superuser"]


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT serializer that enriches token payloads and response data with
    user profile details and active multi-tenant school memberships.
    """
    username_field = "email"

    @classmethod
    def get_token(cls, user: User):
        token = super().get_token(user)
        token["email"] = user.email
        token["full_name"] = user.full_name
        token["is_staff"] = user.is_staff
        token["is_superuser"] = user.is_superuser
        return token

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        data = super().validate(attrs)

        user = self.user
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

        data["user"] = UserSummarySerializer(user).data
        data["schools"] = schools_data
        data["active_school"] = schools_data[0] if len(schools_data) > 0 else None
        return data


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for self-service School Owner registration.
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={"input_type": "password"},
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
    )

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "cnic",
            "password",
            "password_confirm",
        ]
        read_only_fields = ["id"]

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError({"password_confirm": "Passwords do not match."})
        return attrs

    def create(self, validated_data: dict[str, Any]) -> User:
        validated_data.pop("password_confirm")
        password = validated_data.pop("password")
        user = User.objects.create_user(password=password, **validated_data)
        return user
