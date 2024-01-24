from django.contrib import admin
from .models import (
    Guest,
    Floor,
    RoomType,
    Room,
    Amenity,
    Reservation,
    Installment,
    Payment,
    Refund,
    Review,
)


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ("user", "status", "contact_info")


@admin.register(Floor)
class FloorAdmin(admin.ModelAdmin):
    list_display = ("level", "description")


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ("room_type", "price", "description")
    search_fields = ("room_type",)


class AmenityInline(admin.TabularInline):
    model = Amenity
    extra = 1


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("room_label", "floor", "room_type", "capacity", "availability")
    search_fields = ["room_type__room_type"]
    list_filter = ("availability", "capacity")
    inlines = [AmenityInline]

    class Meta:
        verbose_name_plural = "Rooms"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
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
class ReservationAdmin(admin.ModelAdmin):
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
class InstallmentAdmin(admin.ModelAdmin):
    list_display = (
        "reservation",
        "installment_type",
        "installment_amount",
        "installment_status",
    )

    readonly_fields = ["installment_status"]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("installment", "payment_amount", "payment_method")
    search_fields = ["installment"]
    readonly_fields = ["payment_id", "payment_amount", "is_refunded"]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "payment_id",
                    "installment",
                    "created_at",
                    "payment_amount",
                    "payment_method",
                    "is_refunded",
                )
            },
        ),
    )


@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
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
