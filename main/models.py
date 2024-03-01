import uuid
from django.db import models
from django.db.models import Sum
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.crypto import get_random_string
from datetime import datetime


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Guest(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    contact_info = models.CharField(max_length=100, null=True, blank=True)
    nid = models.CharField(max_length=100, unique=True, null=True, blank=True)
    preferences = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to="guests", null=True, blank=True)

    status = models.BooleanField(default=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        ordering = ["-updated_at"]
        verbose_name_plural = "Guests"
        verbose_name = "Guest"


class Floor(models.Model):
    level = models.PositiveIntegerField(
        default=1,
        help_text=_(
            "Floor level, indicating the position of the floor in the building."
        ),
        unique=True,
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text=_("Description of the floor, providing additional information."),
    )

    def __str__(self):
        return f"Level {self.level}"

    class Meta:
        verbose_name_plural = "Floors"
        verbose_name = "Floor"
        ordering = ["level"]


class RoomType(models.Model):
    room_type = models.CharField(
        max_length=100,
        help_text=_("Type of the room, describing its category or purpose."),
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text=_("Price per night for this room type."),
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text=_("Additional details about the room type."),
    )

    def __str__(self):
        return self.room_type

    class Meta:
        verbose_name_plural = "Room Types"
        verbose_name = "Room Type"
        ordering = ["room_type"]


class Room(models.Model):
    floor = models.ForeignKey(
        Floor,
        on_delete=models.CASCADE,
        related_name="rooms",
        help_text=_("The floor to which this room belongs."),
    )
    room_label = models.CharField(
        max_length=1,
        help_text=_("A label uniquely identifying the room on its floor."),
    )
    room_type = models.ForeignKey(
        RoomType,
        on_delete=models.CASCADE,
        help_text=_("The type or category of the room."),
    )
    capacity = models.PositiveIntegerField(
        help_text=_("Maximum number of occupants the room can accommodate."),
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text=_("Additional information or features of the room."),
    )
    is_available = models.BooleanField(
        default=True,
        help_text=_("Indicates whether the room is currently available for booking."),
    )

    def __str__(self):
        return f"{self.floor} - Room {self.room_label} ({self.room_type})"

    class Meta:
        unique_together = ["floor", "room_label"]
        verbose_name_plural = "Rooms"
        verbose_name = "Room"
        ordering = ["floor", "room_label"]


class RoomImage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="room/images/", blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return str(self.room)

    class Meta:
        verbose_name_plural = "Room Images"
        verbose_name = "Room Image"
        ordering = ["room"]


class RoomAmenity(models.Model):
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="amenities",
        help_text=_("The room to which this amenity is associated."),
    )
    title = models.CharField(
        max_length=100,
        help_text=_("Title of the amenity, providing a brief name or description."),
    )
    description = models.CharField(
        max_length=250,
        blank=True,
        null=True,
        help_text=_("Detailed description of the amenity."),
    )
    is_available = models.BooleanField(
        default=True,
        help_text=_("Indicates whether the amenity is currently available."),
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["room", "title"]
        verbose_name = "Amenity"
        verbose_name_plural = "Amenities"


class Review(BaseModel):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="reviews")
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField(
        validators=[
            MinValueValidator(1, message="Rating must be at least 1."),
            MaxValueValidator(10, message="Rating must be at most 10."),
        ]
    )
    comment = models.TextField(blank=True, null=True)
    likes = models.ManyToManyField(Guest, blank=True, related_name="review_likes")

    def __str__(self):
        return str(self.room)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Reviews"
        verbose_name = "Review"


class ReviewImage(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="room/review/images/", blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return str(self.review)

    class Meta:
        verbose_name_plural = "Review Images"
        verbose_name = "Review Image"
        ordering = ["review"]


class Reservation(models.Model):

    def generate_unique_id():
        date_str = datetime.now().strftime("%Y%m%d%H%M%S")
        random_str = get_random_string(6, "0123456789")
        return f"res-{date_str}-{random_str}"

    class ReservationStatusChoices(models.TextChoices):
        RESERVED = "Reserved", "Reserved"
        CHECKED_IN = "Checked-In", "Checked-In"
        CHECKED_OUT = "Checked-Out", "Checked-Out"
        CANCELED = "Canceled", "Canceled"

    id = models.CharField(
        primary_key=True, default=generate_unique_id, editable=False, max_length=50
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    guest = models.ForeignKey(Guest, on_delete=models.PROTECT, null=True, blank=True)
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name="reservations"
    )
    start_date = models.DateField()
    end_date = models.DateField()
    reservation_status = models.CharField(
        max_length=20,
        choices=ReservationStatusChoices.choices,
        default=ReservationStatusChoices.RESERVED,
    )
    payment_status = models.CharField(max_length=20, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    total_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    @property
    def total_amount(self):
        return self.room.room_type.price * (self.end_date - self.start_date).days

    # not permitted to change the reservation status to checked-in if payment status is pending
    def clean(self):
        if self.reservation_status == "Checked-In" and self.payment_status == "Pending":
            raise ValidationError(
                "Reservation status cannot be checked-in if payment status is pending."
            )

    class Meta:
        verbose_name_plural = "Reservations"
        verbose_name = "Reservation"
        ordering = ["-created_at"]
        get_latest_by = "start_date"

    def __str__(self):
        return f"{self.room}-{self.start_date}-{self.total_amount}"


class Installment(BaseModel):

    def generate_unique_id():
        date_str = datetime.now().strftime("%Y%m%d%H%M%S")
        random_str = get_random_string(6, "0123456789")
        return f"ins-{date_str}-{random_str}"

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
        Reservation, on_delete=models.CASCADE, related_name="installments"
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
