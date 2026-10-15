"""
Serializers for Academics app.
"""
from rest_framework import serializers

from .models import AcademicClass, AcademicYear, Section, Subject


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ["id", "name", "room_number", "capacity", "created_at"]
        read_only_fields = ["id", "created_at"]


class SectionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ["id", "academic_class", "name", "room_number", "capacity", "created_at"]
        read_only_fields = ["id", "created_at"]


class AcademicClassSerializer(serializers.ModelSerializer):
    sections = SectionSerializer(many=True, read_only=True)
    section_count = serializers.IntegerField(source="sections.count", read_only=True)

    class Meta:
        model = AcademicClass
        fields = ["id", "name", "code", "order", "sections", "section_count", "created_at"]
        read_only_fields = ["id", "created_at"]


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ["id", "name", "code", "is_elective", "created_at"]
        read_only_fields = ["id", "created_at"]


class AcademicYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicYear
        fields = ["id", "name", "start_date", "end_date", "is_current", "created_at"]
        read_only_fields = ["id", "created_at"]

