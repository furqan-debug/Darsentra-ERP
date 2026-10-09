"""
Serializers for Accounts app.
"""
from rest_framework import serializers

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
            "is_active",
            "date_joined",
        ]
        read_only_fields = ["id", "email", "date_joined", "is_active"]
