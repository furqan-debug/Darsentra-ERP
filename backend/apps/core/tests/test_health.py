"""
Automated tests for health check endpoint.
"""
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class HealthCheckTests(APITestCase):
    def test_health_check_returns_healthy(self):
        """Verify that the health check endpoint returns 200 with healthy database."""
        url = reverse("core:health_check")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("status"), "healthy")
        self.assertEqual(response.data.get("service"), "darsentra-backend")
        self.assertEqual(response.data.get("database", {}).get("status"), "connected")
        self.assertIn("timestamp", response.data)
