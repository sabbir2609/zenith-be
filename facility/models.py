import uuid
from django.db import models
from django.conf import settings
from django.utils.crypto import get_random_string
from django.forms import ValidationError

from datetime import datetime


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Facility(models.Model):
    name = models.CharField(max_length=100, help_text="Name of the facility")
    description = models.CharField(
        max_length=255, null=True, blank=True, help_text="Description of the facility"
    )
    is_reservable = models.BooleanField(
        default=False, help_text="Is the facility reservable?"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Facility"
        verbose_name_plural = "Facilities"
        ordering = ["name"]


class FacilityAmenities(BaseModel):
    facility = models.ForeignKey(
        Facility,
        on_delete=models.CASCADE,
        related_name="amenities",
        help_text="Facility associated with the amenities",
    )
    amenities = models.CharField(max_length=100, help_text="Type of amenities")
    description = models.CharField(
        max_length=255, null=True, blank=True, help_text="Description of the amenities"
    )

    def __str__(self):
        return self.amenities

    class Meta:
        verbose_name = "Facility Amenities"
        verbose_name_plural = "Facility Amenities"
        ordering = ["amenities"]


class FacilityImage(BaseModel):
    facility = models.ForeignKey(
        Facility,
        on_delete=models.CASCADE,
        related_name="images",
        help_text="Facility associated with the image",
    )
    image = models.ImageField(
        upload_to="facilities/images/", help_text="Image file for the facility"
    )
    description = models.CharField(
        max_length=255, null=True, blank=True, help_text="Description of the image"
    )

    def __str__(self):
        return f"{self.facility.name} - Image {self.id}"

    class Meta:
        verbose_name = "Facility Image"
        verbose_name_plural = "Facility Images"
        ordering = ["facility", "id"]


class FacilityReview(BaseModel):
    facility = models.ForeignKey(
        Facility,
        on_delete=models.CASCADE,
        related_name="reviews",
        help_text="Facility associated with the review",
    )
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text="User who wrote the review",
    )
    description = models.CharField(
        max_length=255, null=True, blank=True, help_text="Description of the review"
    )
    rating = models.DecimalField(
        max_digits=2, decimal_places=1, help_text="Rating of the facility"
    )

    def __str__(self):
        return f"{self.facility.name} - Review by {self.reviewer}"

    class Meta:
        verbose_name = "Facility Review"
        verbose_name_plural = "Facility Reviews"
        ordering = ["-rating"]


class FacilityReservation(BaseModel):
    facility = models.ForeignKey(
        Facility,
        on_delete=models.CASCADE,
        related_name="reservations",
        help_text="Facility associated with the reservation",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text="User who made the reservation",
    )
    date = models.DateField(help_text="Date of the reservation")
    start_time = models.TimeField(help_text="Start time of the reservation")
    end_time = models.TimeField(help_text="End time of the reservation")

    # only reservable facilities can be reserved
    def clean(self):
        if not self.facility.is_reservable:
            raise ValidationError("This facility is not reservable")

    def __str__(self):
        return (
            f"{self.facility.name} - {self.date} - {self.start_time} to {self.end_time}"
        )

    class Meta:
        verbose_name = "Facility Reservation"
        verbose_name_plural = "Facility Reservations"
        ordering = ["facility", "date", "start_time"]


def generate_unique_id():
    date_str = datetime.now().strftime("%Y%m%d%H%M%S")
    random_str = get_random_string(6, "0123456789")
    return f"ins-{date_str}-{random_str}"


class Installment(BaseModel):
    class InstallmentChoices(models.TextChoices):
        FIRST = "First", "First"
        SECOND = "Second", "Second"
        THIRD = "Third", "Third"
        FULL = "Full", "Full"

    id = models.CharField(
        default=generate_unique_id,
        primary_key=True,
        editable=False,
        max_length=50,
        unique=True,
    )
    installment_type = models.CharField(
        max_length=20,
        choices=InstallmentChoices.choices,
        default=InstallmentChoices.FIRST,
    )
    reservation = models.ForeignKey(
        FacilityReservation, on_delete=models.CASCADE, related_name="installments"
    )
    installment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    installment_status = models.CharField(max_length=20, default="Pending")

    class Meta:
        verbose_name_plural = "Installments"
        verbose_name = "Installment"
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.reservation} - {self.installment_type} - {self.installment_amount}"
        )


class Payment(BaseModel):

    class PaymentMethodChoices(models.TextChoices):
        CASH = "Cash", "Cash"
        CARD = "Card", "Card"
        MOBILE_BANKING = "Mobile Banking", "Mobile Banking"

    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, editable=False, unique=True
    )
    installment = models.OneToOneField(
        Installment, on_delete=models.CASCADE, related_name="payment"
    )
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethodChoices.choices,
        default=PaymentMethodChoices.CASH,
    )

    is_refunded = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.payment_amount = self.installment.installment_amount
        super(Payment, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Payments"
        verbose_name = "Payment"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.installment}-{self.installment.installment_status}-{self.payment_amount}"


class Refund(BaseModel):
    class RefundMethodChoices(models.TextChoices):
        CASH = "Cash", "Cash"
        CARD = "Card", "Card"
        MOBILE_BANKING = "Mobile Banking", "Mobile Banking"

    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, editable=False, unique=True
    )
    payment = models.OneToOneField(
        Payment, on_delete=models.CASCADE, related_name="refund"
    )
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2)
    refund_method = models.CharField(
        max_length=20,
        choices=RefundMethodChoices.choices,
        default=RefundMethodChoices.CASH,
    )

    class Meta:
        verbose_name_plural = "Refunds"
        verbose_name = "Refund"
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.payment.payment_id)
