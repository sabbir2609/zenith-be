from django.contrib import admin
from .models import DeviceType, Device, Topic, RoomDevice, FacilityDevice


@admin.register(DeviceType)
class DeviceTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name", "description")


class TopicInline(admin.TabularInline):
    model = Topic
    extra = 1


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = (
        "client_id",
        "name",
        "device_type",
        "qos",
        "status",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "id",
                    "name",
                    "device_type",
                    "client_id",
                    "qos",
                    "status",
                    "description",
                    "installation_date",
                )
            },
        ),
    )
    readonly_fields = ("id",)
    search_fields = ("name", "client_id", "description")
    list_filter = ("device_type", "status")
    ordering = ["-created_at"]
    list_per_page = 10

    inlines = [TopicInline]


@admin.register(RoomDevice)
class RoomDeviceAdmin(admin.ModelAdmin):
    list_display = (
        "room",
        "device",
    )
    list_filter = (
        "room__room_label",
        "device__name",
    )
    search_fields = ("room__room_label", "device__name")
    autocomplete_fields = ["room", "device"]


@admin.register(FacilityDevice)
class FacilityDeviceAdmin(admin.ModelAdmin):
    list_display = (
        "facility",
        "device",
    )
    list_filter = (
        "facility__name",
        "device__name",
    )
    search_fields = ("facility__name", "device__name")
