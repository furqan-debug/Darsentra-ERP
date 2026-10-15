"""
Service layer for Accounts app.
Encapsulates business logic for user management.
"""

from .models import User


class UserService:
    @staticmethod
    def create_user(
        email: str,
        password: str | None = None,
        first_name: str = "",
        last_name: str = "",
        phone_number: str = "",
        **extra_fields
    ) -> User:
        """Create a user with standardized attributes."""
        return User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            **extra_fields,
        )
