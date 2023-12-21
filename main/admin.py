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


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("room", "user", "reservation_status")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "room",
                    "user",
                    "start_date",
                    "end_date",
                    "reservation_status",
                )
            },
        ),
    )
