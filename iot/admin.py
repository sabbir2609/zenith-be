from django.contrib import admin
from .models import DeviceType, Device, RoomDevice, FacilityDevice


@admin.register(DeviceType)
class DeviceTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name", "description")


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "device_type",
        "device_id",
        "status",
        "created_at",
        "updated_at",
    )
    search_fields = ("name", "device_id", "description")
    list_filter = ("device_type", "status")
    ordering = ["-created_at"]


@admin.register(RoomDevice)
class RoomDeviceAdmin(admin.ModelAdmin):
    list_display = ("room", "device", "installation_date", "is_active")
    list_filter = ("room__room_label", "device__name", "is_active")
    search_fields = ("room__room_label", "device__name")
    ordering = ["-installation_date"]
    date_hierarchy = "installation_date"


@admin.register(FacilityDevice)
class FacilityDeviceAdmin(admin.ModelAdmin):
    list_display = ("facility", "device", "installation_date", "is_active")
    list_filter = ("facility__name", "device__name", "is_active")
    search_fields = ("facility__name", "device__name")
    ordering = ["-installation_date"]
    date_hierarchy = "installation_date"
