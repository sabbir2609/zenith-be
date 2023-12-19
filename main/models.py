import uuid
from django.db import models
from django.db.models import Sum
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _


class Guest(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=100)
    preferences = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Guest"


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


class Room(models.Model):
    floor = models.ForeignKey(
        Floor,
        on_delete=models.CASCADE,
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
    images = models.ImageField(
        upload_to="room/",
        blank=True,
        null=True,
        help_text=_("Images showcasing the room's interior or features."),
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text=_("Additional information or features of the room."),
    )
    availability = models.BooleanField(
        default=True,
        help_text=_("Indicates whether the room is currently available for booking."),
    )

    def __str__(self):
        return f"{self.floor} - Room {self.room_label} ({self.room_type})"

    class Meta:
        verbose_name_plural = "Rooms"


class Amenity(models.Model):
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
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
    availability = models.BooleanField(
        default=True,
        help_text=_("Indicates whether the amenity is currently available."),
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Amenities"


class Reservation(models.Model):
    class ReservationStatusChoices(models.TextChoices):
        RESERVED = "Reserved", "Reserved"
        CHECKED_IN = "Checked-In", "Checked-In"
        CHECKED_OUT = "Checked-Out", "Checked-Out"
        CANCELED = "Canceled", "Canceled"

    class PaymentStatusChoices(models.TextChoices):
        PENDING = "Pending", "Pending"
        PARTIAL = "Partial", "Partial"
        PAID = "Paid", "Paid"

    guest = models.ForeignKey("Guest", on_delete=models.CASCADE)
    room = models.ForeignKey("Room", on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reservation_status = models.CharField(
        max_length=20,
        choices=ReservationStatusChoices.choices,
        default=ReservationStatusChoices.RESERVED,
    )
    payment_status = models.CharField(max_length=20)

    def get_total_amount(self):
        total_amount = (
            self.room.room_type.price * (self.end_date - self.start_date).days
        )
        return total_amount

    def get_paid_amount(self):
        if not self.pk:
            return 0

        paid_amount = self.installment_set.aggregate(Sum("installment_amount"))[
            "installment_amount__sum"
        ]
        if paid_amount is None:
            paid_amount = 0
            return paid_amount
        return paid_amount

    @property
    def get_payment_status(self):
        total_amount = self.get_total_amount()
        paid_amount = self.get_paid_amount()

        if total_amount == paid_amount:
            self.payment_status = self.PaymentStatusChoices.PAID
            return self.payment_status
        elif total_amount >= paid_amount > 0:
            self.payment_status = self.PaymentStatusChoices.PARTIAL
            return self.payment_status
        elif paid_amount == 0:
            self.payment_status = self.PaymentStatusChoices.PENDING
            return self.payment_status
        else:
            raise ValueError(
                "Invalid payment status: Total amount and paid amount conditions not met"
            )

    def save(self, *args, **kwargs):
        self.payment_status = self.get_payment_status
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Reservations"
        ordering = ["start_date"]
        get_latest_by = "start_date"

    def __str__(self):
        return f"{self.room}-{self.guest}-{self.start_date}"


class Installment(models.Model):
    class InstallmentChoices(models.TextChoices):
        FIRST = "First", "First"
        SECOND = "Second", "Second"
        THIRD = "Third", "Third"

    installment_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    installment_type = models.CharField(
        max_length=20,
        choices=InstallmentChoices.choices,
        default=InstallmentChoices.FIRST,
        unique=True,
    )
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    installment_date = models.DateField(auto_now_add=True)
    installment_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def reservation_installment_count(self):
        return Installment.objects.filter(reservation=self.reservation).count()

    def save(self, *args, **kwargs):
        if self.reservation_installment_count() >= 3:
            raise ValidationError(
                "Cannot add more than three installments for a reservation."
            )
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Installments"
        ordering = ["installment_date"]

    def __str__(self):
        return (
            f"{self.reservation} - {self.installment_type} - {self.installment_amount}"
        )


class Payment(models.Model):
    payment_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    installment = models.OneToOneField(Installment, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)
    payment_method = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Payments"
        ordering = ["payment_date"]

    def __str__(self):
        return str(self.payment_id)


class Review(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[
            MinValueValidator(1, message="Rating must be at least 1."),
            MaxValueValidator(10, message="Rating must be at most 10."),
        ]
    )
    comment = models.TextField(blank=True, null=True)
    images = models.ImageField(upload_to="room/review/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.room)

    class Meta:
        verbose_name_plural = "Reviews"
