from django.contrib import admin
from .models import (
    Facility,
    FacilityAmenities,
    FacilityImage,
    FacilityReview,
)


class FacilityAmenitiesInline(admin.TabularInline):
    model = FacilityAmenities
    extra = 1


class FacilityImageInline(admin.TabularInline):
    model = FacilityImage
    extra = 1


class FacilityReviewInline(admin.TabularInline):
    model = FacilityReview
    extra = 1


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ("name", "is_reservable", "id")
    search_fields = ("name",)
    inlines = [FacilityAmenitiesInline, FacilityImageInline, FacilityReviewInline]


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


@admin.register(FacilityReview)
class FacilityReviewAdmin(admin.ModelAdmin):
    list_display = ("facility", "reviewer", "rating")
    list_filter = ("facility",)
    search_fields = ("facility__name", "reviewer")
    ordering = ("-rating",)
