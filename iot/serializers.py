from iot.models import DeviceType, Device, RoomDevice, FacilityDevice
from rest_framework import serializers


class DeviceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceType
        fields = "__all__"


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = "__all__"


class RoomDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomDevice
        fields = "__all__"


class FacilityDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacilityDevice
        fields = "__all__"
