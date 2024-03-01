from django.contrib import admin
from .models import (
    Facility,
    FacilityExtraCharge,
    FacilityAmenities,
    FacilityImage,
    FacilityReview,
    FacilityReviewImage,
    FacilityReservation,
)

from django.utils.html import format_html


class FacilityAmenitiesInline(admin.TabularInline):
    model = FacilityAmenities
    extra = 1


class FacilityImageInline(admin.TabularInline):
    model = FacilityImage
    extra = 1


class FacilityExtraChargeInline(admin.TabularInline):
    model = FacilityExtraCharge
    extra = 1


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ("name", "is_reservable", "id")
    search_fields = ("name",)
    inlines = [FacilityAmenitiesInline, FacilityImageInline, FacilityExtraChargeInline]


@admin.register(FacilityAmenities)
class FacilityAmenitiesAdmin(admin.ModelAdmin):
    list_display = ("facility", "amenities", "description")
    list_filter = ("facility",)
    search_fields = ("amenities",)


@admin.register(FacilityImage)
class FacilityImageAdmin(admin.ModelAdmin):
    list_display = ("facility", "image", "description")
    list_filter = ("facility",)
    search_fields = ("facility__name",)


class FacilityReviewImageInline(admin.TabularInline):
    model = FacilityReviewImage
    extra = 1
    readonly_fields = ["thumbnail"]

    def thumbnail(self, instance):
        if instance.image.name != "":
            return format_html(
                f'<img src="{instance.image.url}" style=" width: 100px; height: 100px; object-fit: cover;"/>'
            )
        return ""


@admin.register(FacilityReview)
class FacilityReviewAdmin(admin.ModelAdmin):
    list_display = ("facility", "reviewer", "rating")
    list_filter = ("facility",)
    search_fields = ("facility__name", "reviewer")
    ordering = ("-rating",)

    inlines = [FacilityReviewImageInline]
