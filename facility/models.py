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
    description = models.TextField(
        null=True, blank=True, help_text="Description of the facility"
    )

    # if the facility is reservable, then the base reservation fee is required
    is_reservable = models.BooleanField(
        default=False, help_text="Is the facility reservable?"
    )

    base_capacity = models.PositiveIntegerField(
        help_text="Base capacity of the facility", null=True, blank=True
    )
    max_capacity = models.PositiveIntegerField(
        help_text="Maximum capacity of the facility", null=True, blank=True
    )
    opening_time = models.TimeField(
        help_text="Opening time of the facility", null=True, blank=True
    )
    closing_time = models.TimeField(
        help_text="Closing time of the facility", null=True, blank=True
    )

    base_reservation_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Base reservation fee for the facility per hour and base capacity.",
    )

    extra_person_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Extra person fee for the facility",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Facility"
        verbose_name_plural = "Facilities"
        ordering = ["name"]


class FacilityExtraCharge(BaseModel):
    facility = models.ForeignKey(
        Facility,
        on_delete=models.CASCADE,
        related_name="extra_charges",
        help_text="Facility associated with the fee",
    )
    charge = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Fee for the facility"
    )
    description = models.CharField(
        max_length=255, null=True, blank=True, help_text="Description of the fee"
    )

    def __str__(self):
        return f"{self.facility.name} - Charge"

    class Meta:
        verbose_name = "Facility Charge"
        verbose_name_plural = "Facility Charges"
        ordering = ["facility", "charge"]


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


class FacilityReviewImage(BaseModel):
    review = models.ForeignKey(
        FacilityReview,
        on_delete=models.CASCADE,
        related_name="images",
        help_text="Review associated with the image",
    )
    image = models.ImageField(
        upload_to="facilities/reviews/images/", help_text="Image file for the review"
    )
    description = models.CharField(
        max_length=255, null=True, blank=True, help_text="Description of the image"
    )

    def __str__(self):
        return f"{self.review.facility.name} - Image {self.id}"

    class Meta:
        verbose_name = "Facility Review Image"
        verbose_name_plural = "Facility Review Images"
        ordering = ["review", "id"]


class FacilityReservation(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    facility = models.ForeignKey(
        Facility,
        on_delete=models.CASCADE,
        related_name="reservations",
        help_text="Facility associated with the reservation",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text="User who reserved",
    )

    date = models.DateField(help_text="Date of the reservation")
    start_time = models.TimeField(help_text="Time of the reservation")
    end_time = models.TimeField(help_text="End time of the reservation")

    number_of_people = models.PositiveIntegerField(
        help_text="Number of people for the reservation"
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Total amount for the reservation",
    )

    def clean(self):
        if self.date < datetime.now().date():
            raise ValidationError("Reservation date cannot be in the past.")
        if self.start_time < self.facility.opening_time:
            raise ValidationError(
                "Reservation start time cannot be before facility opening time."
            )
        if self.end_time > self.facility.closing_time:
            raise ValidationError(
                "Reservation end time cannot be after facility closing time."
            )
        if self.facility.is_reservable == False:
            raise ValidationError("Facility is not reservable.")

        # if self.number_of_people > self.facility.max_capacity:
        #     raise ValidationError("Number of people exceeds the facility capacity.")

    def calculate_total_amount(self):
        base_fee = self.facility.base_reservation_fee
        extra_person_fee = self.facility.extra_person_fee
        number_of_people = self.number_of_people
        extra_charge = sum(
            [charge.charge for charge in self.facility.extra_charges.all()]
        )
        if extra_charge is None:
            extra_charge = 0
        if extra_person_fee is None:
            extra_person_fee = 0

        total_amount = (
            base_fee + (extra_person_fee * (number_of_people - 1)) + extra_charge
        )
        return total_amount

    def save(self, *args, **kwargs):
        self.total_amount = self.calculate_total_amount()

    def __str__(self):
        return f"{self.facility.name} - Reservation by {self.user}"

    class Meta:
        verbose_name = "Facility Reservation"
        verbose_name_plural = "Facility Reservations"
        ordering = ["date", "start_time"]
