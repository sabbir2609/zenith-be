from django.contrib import admin
from .models import (
    Facility,
    FacilityAmenities,
    FacilityImage,
    FacilityReview,
    FacilityReservation,
    Installment,
    Payment,
    Refund,
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
    list_display = ("name", "description")
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


@admin.register(FacilityReservation)
class FacilityReservationAdmin(admin.ModelAdmin):
    list_display = (
        "facility",
        "user",
        "created_at",
    )
    list_filter = ("facility", "user")
    search_fields = (
        "facility__name",
        "user__username",
        "user__first_name",
        "user__last_name",
    )


@admin.register(Installment)
class InstallmentAdmin(admin.ModelAdmin):
    list_display = ("reservation", "created_at")
    list_filter = ("reservation",)
    search_fields = (
        "reservation__facility__name",
        "reservation__user__username",
        "reservation__user__first_name",
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("installment", "created_at")
    list_filter = ("installment",)
    search_fields = (
        "installment__reservation__facility__name",
        "installment__reservation__user__username",
        "installment__reservation__user__first_name",
    )
