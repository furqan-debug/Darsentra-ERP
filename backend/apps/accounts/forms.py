from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User


class CustomUserCreationForm(UserCreationForm):
    """
    Form for creating new users in Django admin with email as the username.
    """
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "phone_number")


class CustomUserChangeForm(UserChangeForm):
    """
    Form for updating existing users in Django admin.
    """
    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "cnic",
            "is_active",
            "is_staff",
            "is_superuser",
        )
