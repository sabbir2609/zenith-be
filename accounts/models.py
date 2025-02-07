from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.db import models

from .managers import UserManager


# User Model
class User(AbstractBaseUser, PermissionsMixin):
    # User Roles
    ROLE_CHOICES = (
        ("guest", "Guest"),
        ("staff", "Staff"),
        ("admin", "Admin"),
    )

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

    # User Role
    role = models.CharField(
        max_length=20, choices=ROLE_CHOICES, default="guest", help_text="User role."
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
        return f"{self.first_name} {self.last_name} ({self.role})"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def is_staff(self):
        return self.is_admin


# User Profile Model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    # Personal Details
    bio = models.TextField(blank=True, help_text="User's biography.")
    avatar = models.ImageField(
        upload_to="avatars/", blank=True, help_text="User's avatar."
    )

    # Address Details
    house_apt = models.CharField(
        max_length=255, blank=True, help_text="House or apartment number."
    )
    street = models.CharField(max_length=255, blank=True, help_text="Street address.")
    city = models.CharField(max_length=255, blank=True, help_text="City.")
    state = models.CharField(max_length=255, blank=True, help_text="State/Region.")
    zip_code = models.CharField(max_length=20, blank=True, help_text="Postal/ZIP code.")
    country = models.CharField(max_length=255, blank=True, help_text="Country.")

    # Contact Details
    phone = models.CharField(max_length=20, blank=True, help_text="Phone number.")
    emergency_contact = models.CharField(
        max_length=20, blank=True, help_text="Emergency contact number."
    )

    # ID Verification (Guests)
    id_proof_type = models.CharField(
        max_length=50,
        blank=True,
        help_text="Type of ID (Passport, Driver's License, etc.).",
    )
    id_proof_number = models.CharField(
        max_length=100,
        blank=True,
        unique=True,
        help_text="Identification document number.",
    )
    id_proof_image = models.ImageField(
        upload_to="id_proofs/", blank=True, help_text="ID proof image."
    )

    # Guest-Specific Data
    loyalty_points = models.IntegerField(
        default=0, help_text="Loyalty points for returning guests."
    )
    preferred_payment_method = models.CharField(
        max_length=50,
        blank=True,
        help_text="Preferred payment method (Credit Card, PayPal, etc.).",
    )

    # Employment Details (For Hotel Staff)
    employee_id = models.CharField(
        max_length=50, blank=True, unique=True, help_text="Hotel employee ID."
    )
    designation = models.CharField(
        max_length=100, blank=True, help_text="Job title (Receptionist, Manager, etc.)."
    )
    department = models.CharField(
        max_length=100,
        blank=True,
        help_text="Department (Front Desk, Housekeeping, etc.).",
    )
    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Employee salary.",
    )
    hire_date = models.DateField(
        null=True, blank=True, help_text="Employment start date."
    )
    shift = models.CharField(
        max_length=20, blank=True, help_text="Work shift (Morning, Evening, Night)."
    )

    # Medical Information (Optional)
    medical_conditions = models.TextField(
        blank=True, help_text="User's medical conditions."
    )
    allergies = models.TextField(blank=True, help_text="User's allergies.")
    medications = models.TextField(blank=True, help_text="User's medications.")

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return f"{self.user.get_full_name()} Profile"
