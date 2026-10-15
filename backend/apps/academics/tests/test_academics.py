"""
Automated tests for Academics API and strict tenant isolation.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from apps.academics.models import AcademicClass, Section
from apps.schools.models import School, SchoolMembership

User = get_user_model()


class AcademicsTenantIsolationTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            email="owner1@schoola.pk",
            password="SecurePassword123!",
            first_name="School",
            last_name="One",
        )
        self.user2 = User.objects.create_user(
            email="owner2@schoolb.pk",
            password="SecurePassword123!",
            first_name="School",
            last_name="Two",
        )

        self.school1 = School.objects.create(name="School Alpha", code="ALPHA")
        self.school2 = School.objects.create(name="School Beta", code="BETA")

        SchoolMembership.objects.create(user=self.user1, school=self.school1, role="owner")
        SchoolMembership.objects.create(user=self.user2, school=self.school2, role="owner")

        # Academic classes for School Alpha
        self.class_a1 = AcademicClass.objects.create(school=self.school1, name="Class 9", order=9)
        self.sec_a1 = Section.objects.create(school=self.school1, academic_class=self.class_a1, name="Section Red")

        # Academic classes for School Beta
        self.class_b1 = AcademicClass.objects.create(school=self.school2, name="Class 10", order=10)
        self.sec_b1 = Section.objects.create(school=self.school2, academic_class=self.class_b1, name="Section Green")

        self.client = APIClient()

    def test_list_classes_strictly_scoped_to_active_school(self):
        """User 1 should only see classes from School Alpha."""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get("/api/v1/academics/classes/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        class_names = [c["name"] for c in response.data["data"]]
        self.assertIn("Class 9", class_names)
        self.assertNotIn("Class 10", class_names)

    def test_cannot_create_section_in_foreign_school_class(self):
        """User 1 cannot create a section under a class belonging to School Beta."""
        self.client.force_authenticate(user=self.user1)
        payload = {
            "academic_class": self.class_b1.id,
            "name": "Intruder Section",
        }
        response = self.client.post("/api/v1/academics/sections/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_class_and_section_for_own_school(self):
        """User 1 creates Class 11 and Section Gold."""
        self.client.force_authenticate(user=self.user1)
        class_resp = self.client.post(
            "/api/v1/academics/classes/",
            {"name": "Class 11", "order": 11},
            format="json",
        )
        self.assertEqual(class_resp.status_code, status.HTTP_201_CREATED)
        new_class_id = class_resp.data["data"]["id"]

        sec_resp = self.client.post(
            "/api/v1/academics/sections/",
            {"academic_class": new_class_id, "name": "Section Gold"},
            format="json",
        )
        self.assertEqual(sec_resp.status_code, status.HTTP_201_CREATED)

        # Verify in DB that Section Gold belongs to School Alpha
        sec = Section.objects.get(id=sec_resp.data["data"]["id"])
        self.assertEqual(sec.school, self.school1)
