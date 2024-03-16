from iot.models import DeviceType, Device, Topic, RoomDevice, FacilityDevice
from rest_framework import serializers


class DeviceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceType
        fields = "__all__"


class DeviceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ["id", "name", "device_type", "client_id", "status"]


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ["id", "name", "description"]


class DeviceDetailSerializer(serializers.ModelSerializer):
    topics = TopicSerializer(many=True, read_only=True)

    class Meta:
        model = Device
        fields = [
            "id",
            "name",
            "device_type",
            "client_id",
            "status",
            "qos",
            "description",
            "topics",
        ]


class RoomDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomDevice
        fields = "__all__"


class FacilityDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacilityDevice
        fields = "__all__"
