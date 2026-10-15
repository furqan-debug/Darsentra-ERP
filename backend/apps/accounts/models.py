"""
Custom User model for Darsentra ERP.
Provides UUID primary keys, email-based authentication, and fields suited for Pakistani schools.
"""
import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    Primary User model for Darsentra ERP.
    Uses UUID for secure, non-enumerable user identification.
    Email serves as the unique login credential.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
        verbose_name="Email Address",
        max_length=255,
        unique=True,
        db_index=True,
    )
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    phone_number = models.CharField(
        max_length=30,
        blank=True,
        help_text="Pakistani mobile format e.g. +923001234567",
    )
    cnic = models.CharField(
        max_length=20,
        blank=True,
        help_text="Computerized National Identity Card (e.g. 61101-1234567-1)",
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(
        default=False,
        help_text="Designates whether the user can log into the Django admin site.",
    )
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-date_joined"]

    @property
    def full_name(self) -> str:
        """Return user's full name or email if name fields are blank."""
        full = f"{self.first_name} {self.last_name}".strip()
        return full if full else self.email

    def get_full_name(self) -> str:
        return self.full_name

    def get_short_name(self) -> str:
        return self.first_name or self.email

    def __str__(self) -> str:
        return f"{self.full_name} <{self.email}>"
