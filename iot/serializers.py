from iot.models import DeviceType, Device, Topic, RoomDevice, FacilityDevice
from rest_framework import serializers


class DeviceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceType
        fields = "__all__"


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = [
            "id",
            "name",
            "device_type",
            "client_id",
            "qos",
            "status",
            "description",
            "installation_date",
        ]


class DeviceListSerializer(serializers.ModelSerializer):
    location = serializers.SerializerMethodField()
    device_type = serializers.SerializerMethodField()

    class Meta:
        model = Device
        fields = ["id", "name", "device_type", "client_id", "status", "location"]

    def get_device_type(self, obj):
        return obj.device_type.name

    def get_location(self, obj):
        if obj.roomdevice_set.exists():
            return f"{obj.roomdevice_set.first().room.floor} - {obj.roomdevice_set.first().room.room_label} - {obj.roomdevice_set.first().location}"
        elif obj.facilitydevice_set.exists():
            return f"{obj.facilitydevice_set.first().facility.name} - {obj.facilitydevice_set.first().location}"
        else:
            return None


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ["id", "name", "description"]


class DeviceDetailSerializer(serializers.ModelSerializer):
    topics = TopicSerializer(many=True, read_only=True)
    device_type = serializers.SerializerMethodField()

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

    def get_device_type(self, obj):
        return obj.device_type.name


class RoomDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomDevice
        fields = "__all__"


class FacilityDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacilityDevice
        fields = "__all__"
