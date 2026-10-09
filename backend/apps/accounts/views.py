"""
Views for Accounts app.
"""
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSummarySerializer


class CurrentUserView(APIView):
    """
    Returns the authenticated user's profile information.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSummarySerializer(request.user)
        return Response({
            "status": "success",
            "data": serializer.data,
        })
