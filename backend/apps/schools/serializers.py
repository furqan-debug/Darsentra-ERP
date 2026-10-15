"""
Serializers for Schools and Memberships.
"""
from rest_framework import serializers

from .models import School, SchoolMembership


class SchoolSerializer(serializers.ModelSerializer):
    """
    Serializer for School tenant entity.
    """
    curriculum_display = serializers.CharField(source="get_curriculum_type_display", read_only=True)
    province_display = serializers.CharField(source="get_province_display", read_only=True)

    class Meta:
        model = School
        fields = [
            "id",
            "name",
            "slug",
            "code",
            "registration_number",
            "curriculum_type",
            "curriculum_display",
            "contact_email",
            "phone_number",
            "address",
            "city",
            "province",
            "province_display",
            "is_active",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class SchoolMembershipSerializer(serializers.ModelSerializer):
    """
    Serializer for user's membership within a school.
    """
    school = SchoolSerializer(read_only=True)
    role_display = serializers.CharField(source="get_role_display", read_only=True)

    class Meta:
        model = SchoolMembership
        fields = [
            "id",
            "school",
            "role",
            "role_display",
            "is_active",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class SchoolSetupSerializer(serializers.ModelSerializer):
    """
    Serializer for the school setup / onboarding wizard.
    """
    initial_classes = serializers.ListField(
        child=serializers.CharField(max_length=50),
        required=False,
        default=list,
    )
    academic_year_name = serializers.CharField(
        max_length=50,
        required=False,
        default="2026-2027",
    )

    class Meta:
        model = School
        fields = [
            "id",
            "name",
            "code",
            "slug",
            "registration_number",
            "curriculum_type",
            "contact_email",
            "phone_number",
            "address",
            "city",
            "province",
            "initial_classes",
            "academic_year_name",
        ]
        read_only_fields = ["id", "slug"]

    def validate_code(self, value):
        code = value.strip().upper()
        if School.objects.filter(code=code).exists():
            raise serializers.ValidationError("A school with this institutional code already exists.")
        return code
