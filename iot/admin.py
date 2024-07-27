from django.contrib import admin
from .models import DeviceType, Device, Topic, RoomDevice, FacilityDevice
from unfold.admin import ModelAdmin, TabularInline
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.forms.widgets import ArrayWidget, WysiwygWidget
from unfold.contrib.filters.admin import (
    RangeDateFilter,
    RangeDateTimeFilter,  # noqa
)
from unfold.contrib.import_export.forms import ExportForm, ImportForm


@admin.register(DeviceType)
class DeviceTypeAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ("name",)
    search_fields = ("name", "description")

    export_form = ExportForm
    import_form = ImportForm


class TopicInline(TabularInline):
    model = Topic
    extra = 1


@admin.register(Device)
class DeviceAdmin(ModelAdmin, ImportExportModelAdmin):
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

    list_filter = (
        "device_type",
        "status",
        ("installation_date", RangeDateFilter),
    )
    list_filter_submit = True
    list_per_page = 10

    inlines = [TopicInline]

    export_form = ExportForm
    import_form = ImportForm


@admin.register(RoomDevice)
class RoomDeviceAdmin(ModelAdmin):
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
class FacilityDeviceAdmin(ModelAdmin):
    list_display = (
        "facility",
        "device",
    )
    list_filter = (
        "facility__name",
        "device__name",
    )
    search_fields = ("facility__name", "device__name")
