"""
Automated tests for School Onboarding and Setup Wizard API.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from apps.academics.models import AcademicClass, AcademicYear
from apps.schools.models import School, SchoolMembership

User = get_user_model()


class SchoolOnboardingTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="founder@pakistanschool.edu.pk",
            password="StrongPassword123!",
            first_name="Tariq",
            last_name="Javed",
        )
        self.client.force_authenticate(user=self.user)

    def test_active_school_empty_when_no_memberships(self):
        """Active school returns has_school: False when user has no school."""
        response = self.client.get("/api/v1/schools/active/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data["data"]["has_school"])
        self.assertIsNone(response.data["data"]["school"])

    def test_school_setup_creates_school_session_and_classes(self):
        """POST /api/v1/schools/setup/ successfully boots a school tenant."""
        payload = {
            "name": "Beacon Light Academy",
            "code": "BLA-KHI",
            "curriculum_type": "matric_fsc",
            "contact_email": "info@bla.edu.pk",
            "phone_number": "+92 21 34567890",
            "city": "Karachi",
            "address": "Gulshan-e-Iqbal Block 5",
            "academic_year_name": "2026-2027",
            "initial_classes": ["Class 1", "Class 2", "Class 3", "Class 9", "Class 10"],
        }
        response = self.client.post("/api/v1/schools/setup/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], "success")

        school = School.objects.get(code="BLA-KHI")
        self.assertEqual(school.name, "Beacon Light Academy")
        self.assertEqual(school.curriculum_type, "matric_fsc")

        # Verify Owner membership
        membership = SchoolMembership.objects.get(user=self.user, school=school)
        self.assertEqual(membership.role, "owner")

        # Verify Academic Session
        session = AcademicYear.objects.get(school=school, name="2026-2027")
        self.assertTrue(session.is_current)

        # Verify Generated Classes and Sections
        classes = AcademicClass.objects.filter(school=school)
        self.assertEqual(classes.count(), 5)
        for cls in classes:
            self.assertEqual(cls.sections.count(), 1)
            self.assertEqual(cls.sections.first().name, "Section A")

        # Verify Active School now returns full data
        active_resp = self.client.get("/api/v1/schools/active/")
        self.assertEqual(active_resp.status_code, status.HTTP_200_OK)
        self.assertTrue(active_resp.data["data"]["has_school"])
        self.assertEqual(active_resp.data["data"]["stats"]["total_classes"], 5)
        self.assertEqual(active_resp.data["data"]["stats"]["total_sections"], 5)
