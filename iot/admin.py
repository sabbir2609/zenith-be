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
        "client_id",
        "status",
        "created_at",
        "updated_at",
    )
    search_fields = ("name", "client_id", "description")
    list_filter = ("device_type", "status")
    ordering = ["-created_at"]


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
