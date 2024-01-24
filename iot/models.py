from django.db import models
from django.core.exceptions import ValidationError
from main.models import Room
from facility.models import Facility
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class DeviceType(models.Model):
    name = models.CharField(max_length=100, help_text=_("Name of the device type"))
    description = models.TextField(
        null=True, blank=True, help_text=_("Description of the device type")
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Device Type")
        verbose_name_plural = _("Device Types")
        ordering = ["id"]


class Device(BaseModel):
    name = models.CharField(max_length=100, help_text=_("Name of the device"))
    device_type = models.ForeignKey(
        DeviceType, on_delete=models.CASCADE, help_text=_("Type of the device")
    )
    device_id = models.CharField(
        max_length=100, help_text=_("Unique identifier for the device")
    )
    description = models.TextField(
        null=True, blank=True, help_text=_("Description of the device")
    )
    status = models.BooleanField(
        default=False, help_text=_("Status of the device (active/inactive)")
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Device")
        verbose_name_plural = _("Devices")
        ordering = ["-created_at"]


class BaseDeviceInstallation(BaseModel):
    installation_date = models.DateField(
        help_text=_("Date when the device was installed")
    )
    is_active = models.BooleanField(
        default=True, help_text=_("Indicates whether the device is currently active")
    )

    class Meta:
        abstract = True


class RoomDevice(BaseDeviceInstallation):
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="devices",
        help_text=_("Room in which the device is installed"),
    )
    device = models.ForeignKey(
        Device, on_delete=models.CASCADE, help_text=_("Device installed in the room")
    )

    def clean(self):
        # Check if the device is already installed in a facility
        if FacilityDevice.objects.filter(device=self.device).exists():
            raise ValidationError(_("This device is already installed in a facility."))

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.room} - {self.device}"

    class Meta:
        verbose_name = _("Room Device")
        verbose_name_plural = _("Room Devices")
        unique_together = ("room", "device")


class FacilityDevice(BaseDeviceInstallation):
    facility = models.ForeignKey(
        Facility,
        on_delete=models.CASCADE,
        related_name="devices",
        help_text=_("Facility where the device is installed"),
    )
    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        help_text=_("Device installed in the facility"),
    )

    def clean(self):
        # Check if the device is already installed in a room
        if RoomDevice.objects.filter(device=self.device).exists():
            raise ValidationError(_("This device is already installed in a room."))

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.facility} - {self.device}"

    class Meta:
        verbose_name = _("Facility Device")
        verbose_name_plural = _("Facility Devices")
        unique_together = ("facility", "device")
