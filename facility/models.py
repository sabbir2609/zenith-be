from django.db import models
from django.conf import settings


class Facility(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Facility"
        verbose_name_plural = "Facilities"
        ordering = ["name"]


class FacilityAmenities(models.Model):
    facility = models.ForeignKey(
        Facility, on_delete=models.CASCADE, related_name="amenities"
    )
    amenities = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.amenities

    class Meta:
        verbose_name = "Facility Amenities"
        verbose_name_plural = "Facility Amenities"
        ordering = ["amenities"]


class FacilityImage(models.Model):
    facility = models.ForeignKey(
        Facility, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="facilities/images/")
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.facility.name} - Image {self.id}"

    class Meta:
        verbose_name = "Facility Image"
        verbose_name_plural = "Facility Images"
        ordering = ["facility", "id"]


class FacilityReview(models.Model):
    facility = models.ForeignKey(
        Facility, on_delete=models.CASCADE, related_name="reviews"
    )
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    review_text = models.TextField()
    rating = models.FloatField()

    def __str__(self):
        return f"{self.facility.name} - Review by {self.reviewer_name}"

    class Meta:
        verbose_name = "Facility Review"
        verbose_name_plural = "Facility Reviews"
        ordering = ["-rating"]
