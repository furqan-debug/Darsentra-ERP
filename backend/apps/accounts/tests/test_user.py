"""
Automated tests for Custom User model.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class UserModelTests(TestCase):
    def test_create_user_successful(self):
        """Test creating a standard user with email and password."""
        email = "teacher@school.edu.pk"
        password = "SecurePassword123!"
        user = User.objects.create_user(
            email=email,
            password=password,
            first_name="Ahmed",
            last_name="Khan",
            phone_number="+923001234567",
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)
        self.assertEqual(user.full_name, "Ahmed Khan")
        self.assertEqual(str(user), "Ahmed Khan <teacher@school.edu.pk>")

    def test_create_user_without_email_raises_error(self):
        """Test that creating a user without email raises ValueError."""
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="password123")

    def test_create_superuser_successful(self):
        """Test creating a superuser with full permissions."""
        email = "admin@darsentra.pk"
        password = "SuperAdminPassword123!"
        admin_user = User.objects.create_superuser(
            email=email,
            password=password,
        )

        self.assertEqual(admin_user.email, email)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_active)

    def test_create_superuser_invalid_staff_flag(self):
        """Test that superuser creation fails if is_staff is False."""
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="admin2@darsentra.pk",
                password="password",
                is_staff=False,
            )

    def test_create_superuser_invalid_superuser_flag(self):
        """Test that superuser creation fails if is_superuser is False."""
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="admin3@darsentra.pk",
                password="password",
                is_superuser=False,
            )
