"""
Core views including system health check endpoint.
"""
import logging

from django.conf import settings
from django.db import connection
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger(__name__)


class HealthCheckView(APIView):
    """
    Public health check endpoint at /api/v1/health/.
    Verifies application state, settings, and database connectivity.
    """
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        db_status = "connected"
        db_error = None
        http_status = status.HTTP_200_OK

        try:
            connection.ensure_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1;")
                cursor.fetchone()
        except Exception as e:
            logger.error("Health check database error: %s", str(e))
            db_status = "disconnected"
            db_error = str(e)
            http_status = status.HTTP_503_SERVICE_UNAVAILABLE

        payload = {
            "status": "healthy" if db_status == "connected" else "unhealthy",
            "service": "darsentra-backend",
            "version": "1.0.0",
            "environment": "development" if settings.DEBUG else "production",
            "database": {
                "status": db_status,
                "engine": connection.vendor,
                "error": db_error,
            },
            "timestamp": timezone.now().isoformat(),
        }

        return Response(payload, status=http_status)
