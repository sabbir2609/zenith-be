from django.contrib import admin
from .models import (
    Guest,
    Floor,
    RoomType,
    Room,
    RoomImage,
    RoomAmenity,
    Reservation,
    Installment,
    Payment,
    Refund,
    Review,
    ReviewImage,
)
from import_export.admin import ImportExportModelAdmin
from unfold.admin import ModelAdmin, TabularInline
from unfold.contrib.filters.admin import RangeDateFilter, RangeDateTimeFilter
from unfold.contrib.forms.widgets import ArrayWidget, WysiwygWidget
from unfold.contrib.import_export.forms import ExportForm, ImportForm


@admin.register(Guest)
class GuestAdmin(ModelAdmin):
    list_display = ("user", "status", "contact_info")


@admin.register(Floor)
class FloorAdmin(ModelAdmin):
    list_display = ("level", "is_elevator_accessible")
    list_editable = ("is_elevator_accessible",)
    list_filter = ("is_elevator_accessible",)


@admin.register(RoomType)
class RoomTypeAdmin(ModelAdmin):
    list_display = ("room_type", "price")
    search_fields = ("room_type",)


class RoomAmenityInline(TabularInline):
    model = RoomAmenity
    extra = 1
    tab = True
    hide_title = True


class RoomImageInline(TabularInline):
    model = RoomImage
    extra = 1
    tab = True
    hide_title = True


@admin.register(Room)
class RoomAdmin(ModelAdmin):
    list_display = (
        "room_label",
        "id",
        "floor",
        "room_type",
        "capacity",
        "is_available",
    )
    search_fields = ["room_type__room_type"]
    list_filter = ("is_available", "capacity", "room_type")
    inlines = [RoomAmenityInline, RoomImageInline]
    list_per_page = 10


class ReviewImageInline(admin.TabularInline):
    model = ReviewImage
    extra = 1
    tab = True
    hide_title = True


@admin.register(Review)
class ReviewAdmin(ModelAdmin):
    list_display = ("room", "guest", "rating", "comment", "created_at")
    search_fields = ["room__room_id"]
    readonly_fields = ["created_at"]


class InstallmentInline(admin.TabularInline):
    model = Installment
    extra = 0
    max_num = 3
    min_num = 1
    readonly_fields = [
        "installment_type",
        "installment_amount",
        "installment_status",
        "created_at",
    ]

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Reservation)
class ReservationAdmin(ModelAdmin):
    def paid_amount(self, obj):
        # Calculate the total paid amount for the reservation
        payments = Payment.objects.filter(installment__reservation=obj)
        return sum(payment.payment_amount for payment in payments)

    list_display = (
        "room",
        "user",
        "reservation_status",
        "total_amount",
        "paid_amount",
        "payment_status",
    )
    inlines = [InstallmentInline]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "room",
                    "user",
                    "start_date",
                    "end_date",
                    "total_amount",
                    "payment_status",
                    "reservation_status",
                )
            },
        ),
    )

    readonly_fields = ["total_amount", "payment_status"]


@admin.register(Installment)
class InstallmentAdmin(ModelAdmin):
    list_display = (
        "reservation",
        "installment_type",
        "installment_amount",
        "installment_status",
    )

    readonly_fields = ["installment_status"]


@admin.register(Payment)
class PaymentAdmin(ModelAdmin):
    list_display = ("installment", "payment_amount", "payment_method")
    search_fields = ["installment"]
    readonly_fields = ["payment_amount", "is_refunded"]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "installment",
                    "payment_amount",
                    "payment_method",
                    "is_refunded",
                )
            },
        ),
    )


@admin.register(Refund)
class RefundAdmin(ModelAdmin):
    list_display = ("payment", "refund_amount", "refund_method")
    search_fields = ["payment"]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "payment",
                    "refund_amount",
                    "created_at",
                    "refund_method",
                )
            },
        ),
    )
    autocomplete_fields = ["payment"]
