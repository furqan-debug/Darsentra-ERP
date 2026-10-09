"""
Standardized API exception handling for Darsentra ERP.
Formats all REST Framework exceptions into a consistent JSON response schema.
"""
import logging
from typing import Any

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)


def custom_exception_handler(exc: Exception, context: dict[str, Any]) -> Response | None:
    """
    Custom exception handler that guarantees all API error responses follow:
    {
        "status": "error",
        "code": "string_error_code",
        "message": "Human-readable description",
        "errors": { ... detailed field or validation errors ... }
    }
    """
    response = exception_handler(exc, context)

    if response is not None:
        code = getattr(exc, "default_code", "error")
        message = "An error occurred while processing your request."

        # Extract cleaner message if available
        if hasattr(exc, "detail"):
            if isinstance(exc.detail, str):
                message = exc.detail
            elif isinstance(exc.detail, dict) and "detail" in exc.detail:
                message = str(exc.detail["detail"])
            elif isinstance(exc.detail, list) and len(exc.detail) > 0:
                message = str(exc.detail[0])

        formatted_data = {
            "status": "error",
            "code": code,
            "message": message,
            "errors": response.data if isinstance(response.data, (dict, list)) else {"detail": str(response.data)},
        }
        response.data = formatted_data
        return response

    # If unhandled server error occurs in non-DEBUG mode
    logger.exception("Unhandled server exception: %s", exc)
    return Response(
        {
            "status": "error",
            "code": "internal_server_error",
            "message": "An internal server error occurred.",
            "errors": {"detail": "Please contact support if the issue persists."},
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
