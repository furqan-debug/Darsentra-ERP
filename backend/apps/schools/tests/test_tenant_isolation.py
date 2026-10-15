"""
Automated tests for Multi-Tenant Data Isolation and Authorization.
Validates that tenant boundaries are strictly enforced and cross-tenant access is prevented.
"""
import uuid

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.schools.models import (
    CurriculumType,
    MembershipRole,
    ProvinceChoices,
    School,
    SchoolMembership,
)

User = get_user_model()


class MultiTenantIsolationTests(APITestCase):
    def setUp(self):
        # Create School 1
        self.school_one = School.objects.create(
            name="Islamabad Model College",
            slug="islamabad-model-college",
            code="IMC-F8-01",
            curriculum_type=CurriculumType.FEDERAL_BOARD,
            city="Islamabad",
            province=ProvinceChoices.ISLAMABAD,
        )

        # Create School 2
        self.school_two = School.objects.create(
            name="Lahore Grammar School",
            slug="lahore-grammar-school",
            code="LGS-JT-01",
            curriculum_type=CurriculumType.CAMBRIDGE,
            city="Lahore",
            province=ProvinceChoices.PUNJAB,
        )

        # User A belongs strictly to School 1
        self.user_a = User.objects.create_user(
            email="principal@imc.edu.pk",
            password="StrongPassword123!",
            first_name="Tariq",
            last_name="Mahmood",
        )
        self.membership_a = SchoolMembership.objects.create(
            user=self.user_a,
            school=self.school_one,
            role=MembershipRole.PRINCIPAL,
            is_active=True,
        )

        # User B belongs strictly to School 2
        self.user_b = User.objects.create_user(
            email="admin@lgs.edu.pk",
            password="StrongPassword123!",
            first_name="Fatima",
            last_name="Zahra",
        )
        self.membership_b = SchoolMembership.objects.create(
            user=self.user_b,
            school=self.school_two,
            role=MembershipRole.ADMIN,
            is_active=True,
        )

        # User C has no school memberships
        self.user_c = User.objects.create_user(
            email="unassigned@darsentra.pk",
            password="StrongPassword123!",
            first_name="Zubair",
            last_name="Ali",
        )

    def test_user_a_can_only_see_their_own_school_in_list(self):
        """User A should only see School 1 in the list of schools."""
        self.client.force_authenticate(user=self.user_a)
        url = reverse("schools:school_list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data.get("data", response.data.get("results", []))
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], str(self.school_one.id))
        self.assertEqual(results[0]["code"], "IMC-F8-01")

    def test_user_b_can_only_see_their_own_school_in_list(self):
        """User B should only see School 2 in the list of schools."""
        self.client.force_authenticate(user=self.user_b)
        url = reverse("schools:school_list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data.get("data", response.data.get("results", []))
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], str(self.school_two.id))
        self.assertEqual(results[0]["code"], "LGS-JT-01")

    def test_user_a_can_access_their_own_school_detail(self):
        """User A can view School 1 detail."""
        self.client.force_authenticate(user=self.user_a)
        url = reverse("schools:school_detail", kwargs={"school_id": self.school_one.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["id"], str(self.school_one.id))

    def test_user_a_cannot_access_school_two_detail(self):
        """
        Cross-tenant access attempt: User A attempting to view School 2
        must be rejected with HTTP 403 Forbidden.
        """
        self.client.force_authenticate(user=self.user_a)
        url = reverse("schools:school_detail", kwargs={"school_id": self.school_two.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data.get("status"), "error")

    def test_user_b_cannot_access_school_one_detail(self):
        """
        Cross-tenant access attempt: User B attempting to view School 1
        must be rejected with HTTP 403 Forbidden.
        """
        self.client.force_authenticate(user=self.user_b)
        url = reverse("schools:school_detail", kwargs={"school_id": self.school_one.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data.get("status"), "error")

    def test_unauthenticated_request_rejected(self):
        """Unauthenticated requests must be denied."""
        url = reverse("schools:school_detail", kwargs={"school_id": self.school_one.id})
        response = self.client.get(url)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_inactive_membership_denied(self):
        """User with inactive membership cannot access school data."""
        self.membership_a.is_active = False
        self.membership_a.save()

        self.client.force_authenticate(user=self.user_a)
        url = reverse("schools:school_detail", kwargs={"school_id": self.school_one.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_nonexistent_school_id_denied(self):
        """Request with a random UUID must be denied, not leak school existence."""
        self.client.force_authenticate(user=self.user_a)
        random_id = uuid.uuid4()
        url = reverse("schools:school_detail", kwargs={"school_id": random_id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
