from django.db import models
from django.conf import settings


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


class FacilityAmenities(models.Model):
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


class FacilityImage(models.Model):
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


class FacilityReview(models.Model):
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
    rating = models.FloatField(help_text="Rating of the facility")

    def __str__(self):
        return f"{self.facility.name} - Review by {self.reviewer_name}"

    class Meta:
        verbose_name = "Facility Review"
        verbose_name_plural = "Facility Reviews"
        ordering = ["-rating"]


class FacilityReservation(models.Model):
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

    def __str__(self):
        return (
            f"{self.facility.name} - {self.date} - {self.start_time} to {self.end_time}"
        )

    class Meta:
        verbose_name = "Facility Reservation"
        verbose_name_plural = "Facility Reservations"
        ordering = ["facility", "date", "start_time"]


class FacilityInstallment(models.Model):
    facility = models.ForeignKey(
        FacilityReservation,
        on_delete=models.CASCADE,
        related_name="installments",
        help_text="Facility associated with the installment",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text="User who made the installment",
    )
    date = models.DateField(help_text="Date of the installment")
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Amount of the installment"
    )

    def __str__(self):
        return f"{self.facility.name} - {self.date} - {self.amount}"

    class Meta:
        verbose_name = "Facility Installment"
        verbose_name_plural = "Facility Installments"
        ordering = ["facility", "date"]
