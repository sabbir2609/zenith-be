from django.db import models
from main.models import Room
from facility.models import Facility


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class DeviceType(models.Model):
    name = models.CharField(max_length=100, help_text="Name of the device type")
    description = models.TextField(
        null=True, blank=True, help_text="Description of the device type"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Device Type"
        verbose_name_plural = "Device Types"
        ordering = ["id"]


class Device(BaseModel):
    name = models.CharField(max_length=100, help_text="Name of the device")
    device_type = models.ForeignKey(
        DeviceType, on_delete=models.CASCADE, help_text="Type of the device"
    )
    device_id = models.CharField(
        max_length=100, help_text="Unique identifier for the device"
    )
    description = models.TextField(
        null=True, blank=True, help_text="Description of the device"
    )
    status = models.BooleanField(
        default=False, help_text="Status of the device (active/inactive)"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Device"
        verbose_name_plural = "Devices"
        ordering = ["-created_at"]


class RoomDevice(models.Model):
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="devices",
        help_text="Room in which the device is installed",
    )
    device = models.ForeignKey(
        Device, on_delete=models.CASCADE, help_text="Device installed in the room"
    )
    installation_date = models.DateField(
        help_text="Date when the device was installed in the room"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Indicates whether the device is currently active in the room",
    )

    def __str__(self):
        return f"{self.room} - {self.device}"

    class Meta:
        verbose_name = "Room Device"
        verbose_name_plural = "Room Devices"
        unique_together = ("room", "device")


class FacilityDevice(models.Model):
    facility = models.ForeignKey(
        Facility,
        on_delete=models.CASCADE,
        related_name="devices",
        help_text="Facility where the device is installed",
    )
    device = models.ForeignKey(
        Device, on_delete=models.CASCADE, help_text="Device installed in the facility"
    )
    installation_date = models.DateField(
        help_text="Date when the device was installed in the facility"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Indicates whether the device is currently active in the facility",
    )

    def __str__(self):
        return f"{self.facility} - {self.device}"

    class Meta:
        verbose_name = "Facility Device"
        verbose_name_plural = "Facility Devices"
        unique_together = ("facility", "device")
