from django.views.generic import TemplateView

from rest_framework import viewsets

from iot.models import DeviceType, Device, RoomDevice, FacilityDevice
from iot.serializers import (
    DeviceTypeSerializer,
    DeviceListSerializer,
    DeviceDetailSerializer,
    RoomDeviceSerializer,
    FacilityDeviceSerializer,
)


class DeviceTypeViewSet(viewsets.ModelViewSet):
    queryset = DeviceType.objects.all()
    serializer_class = DeviceTypeSerializer


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return DeviceListSerializer
        if self.action == "retrieve":
            return DeviceDetailSerializer
        return super().get_serializer_class()


class RoomDeviceViewSet(viewsets.ModelViewSet):
    queryset = RoomDevice.objects.all()
    serializer_class = RoomDeviceSerializer


class FacilityDeviceViewSet(viewsets.ModelViewSet):
    queryset = FacilityDevice.objects.all()
    serializer_class = FacilityDeviceSerializer


class IoTChannel(TemplateView):
    template_name = "iot/page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        device_id = self.kwargs["device_id"]
        topic = Device.objects.get(client_id=device_id).topic

        context["title"] = "IoT Devices Websocket Test"
        context["device_id"] = device_id
        context["topic"] = topic
        return context
