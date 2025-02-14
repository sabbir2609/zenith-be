from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.db import models

from .managers import UserManager


# User Model
class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(
        max_length=255, blank=True, help_text="User's first name."
    )
    last_name = models.CharField(
        max_length=255, blank=True, help_text="User's last name."
    )
    username = models.CharField(
        max_length=255, unique=True, blank=True, null=True, help_text="Username."
    )
    email = models.EmailField(
        unique=True, help_text="User's email address.", db_index=True
    )

    # User Status
    is_active = models.BooleanField(
        default=True, help_text="Whether the user is active."
    )
    is_admin = models.BooleanField(
        default=False, help_text="Whether the user is an admin."
    )

    # Security & Authentication
    is_phone_verified = models.BooleanField(
        default=False, help_text="Whether the user's phone number is verified."
    )
    two_factor_enabled = models.BooleanField(
        default=False, help_text="Whether 2FA is enabled."
    )
    last_password_reset = models.DateTimeField(
        null=True, blank=True, help_text="Timestamp of last password reset."
    )

    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="User creation timestamp."
    )
    last_login = models.DateTimeField(auto_now=True, help_text="Last login timestamp.")

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def is_staff(self):
        return self.is_admin
