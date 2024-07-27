from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from unfold.admin import ModelAdmin, TabularInline
from unfold.contrib.filters.admin import RangeDateFilter, RangeDateTimeFilter
from unfold.contrib.forms.widgets import ArrayWidget, WysiwygWidget
from unfold.contrib.import_export.forms import ExportForm, ImportForm

from .models import (
    Facility,
    FacilityAmenities,
    FacilityExtraCharge,
    FacilityImage,
    FacilityReservation,
    FacilityReview,
    FacilityReviewImage,
)


class FacilityAmenitiesInline(TabularInline):
    model = FacilityAmenities
    extra = 1
    tab = True
    hide_title = True


class FacilityImageInline(TabularInline):
    model = FacilityImage
    extra = 1
    tab = True
    hide_title = True


class FacilityExtraChargeInline(TabularInline):
    model = FacilityExtraCharge
    extra = 1
    tab = True
    hide_title = True


@admin.register(Facility)
class FacilityAdmin(ModelAdmin):
    list_display = ("name", "is_reservable", "id")
    search_fields = ("name",)
    inlines = [FacilityAmenitiesInline, FacilityImageInline, FacilityExtraChargeInline]


# @admin.register(FacilityAmenities)
# class FacilityAmenitiesAdmin(ModelAdmin):
#     list_display = ("facility", "amenities", "description")
#     list_filter = ("facility",)
#     search_fields = ("amenities",)


# @admin.register(FacilityImage)
# class FacilityImageAdmin(ModelAdmin):
#     list_display = ("facility", "image", "description")
#     list_filter = ("facility",)
#     search_fields = ("facility__name",)


class FacilityReviewImageInline(TabularInline):
    model = FacilityReviewImage
    extra = 1
    tab = True
    hide_title = True


@admin.register(FacilityReview)
class FacilityReviewAdmin(ModelAdmin):
    list_display = ("facility", "reviewer", "rating")
    list_filter = ("facility",)
    search_fields = ("facility__name", "reviewer")
    ordering = ("-rating",)

    inlines = [FacilityReviewImageInline]


@admin.register(FacilityReservation)
class FacilityReservationAdmin(ModelAdmin):
    list_display = ("facility", "user", "date", "start_time", "end_time")
    list_filter = ("facility",)
    search_fields = ("facility__name", "user__first_name", "user__last_name")
    ordering = ("date",)
