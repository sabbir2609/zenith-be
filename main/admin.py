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
    Review,
)


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ("name", "contact_info", "preferences")
    search_fields = ("name", "contact_info")


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


class InstallmentInline(admin.TabularInline):
    model = Installment
    extra = 0
    help_texts = "First Save The Reservation Than Add Installment(s)"
    readonly_fields = ["installment_date"]


@admin.register(Installment)
class InstallmentAdmin(admin.ModelAdmin):
    list_display = ("reservation", "installment_date", "installment_amount")
    search_fields = ("reservation__room__room_id", "reservation__guest__name")
    list_filter = (
        "reservation__reservation_status",
        "reservation__payment_status",
    )
    readonly_fields = ["installment_date"]
    fieldsets = (
        (
            "Reservation Information",
            {
                "fields": [
                    ("reservation", "installment_date"),
                ],
            },
        ),
        (
            "Installment Information",
            {
                "fields": [
                    ("installment_amount"),
                ],
            },
        ),
    )


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    def total_amount(self, obj):
        return obj.get_total_amount()

    total_amount.short_description = "Total Amount"

    def paid_amount(self, obj):
        return obj.get_paid_amount()

    paid_amount.short_description = "Paid Amount"

    def due_amount(self, obj):
        return obj.get_total_amount() - obj.get_paid_amount()

    due_amount.short_description = "Due Amount"

    list_display = (
        "room",
        "guest",
        "reservation_status",
        "total_amount",
        "paid_amount",
        "due_amount",
        "payment_status",
    )

    fieldsets = (
        (
            "Reservation Information",
            {
                "fields": [
                    ("room", "guest"),
                    ("start_date", "end_date"),
                ],
            },
        ),
        (
            "Status",
            {
                "fields": [
                    ("reservation_status", "payment_status"),
                ],
            },
        ),
    )

    inlines = [InstallmentInline]
    readonly_fields = ["payment_status"]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("installment", "amount", "payment_date")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("room", "guest", "rating")
    search_fields = ("guest__name", "room__room_id")
