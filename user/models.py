# user/models.py
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(
        max_length=255, blank=True, help_text="The user's first name."
    )
    last_name = models.CharField(
        max_length=255, blank=True, help_text="The user's last name."
    )
    username = models.CharField(
        max_length=255,
        unique=True,
        blank=True,
        null=True,
        help_text="The user's username.",
    )
    email = models.EmailField(unique=True, help_text="The user's email address.")

    is_active = models.BooleanField(
        default=True, help_text="Whether the user is active."
    )

    is_admin = models.BooleanField(
        default=False, help_text="Whether the user is an admin."
    )
    is_superuser = models.BooleanField(
        default=False, help_text="Whether the user is a superuser."
    )

    created_at = models.DateTimeField(
        auto_now_add=True, help_text="The date and time the user was created."
    )
    last_login = models.DateTimeField(
        auto_now=True, help_text="The date and time the user last logged in."
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin
