from django.shortcuts import render
from django.views.generic import TemplateView

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from iot.models import DeviceType, Device, RoomDevice, FacilityDevice
from iot.serializers import (
    DeviceTypeSerializer,
    DeviceSerializer,
    RoomDeviceSerializer,
    FacilityDeviceSerializer,
)

from iot.mqtt.client import client


class DeviceTypeViewSet(viewsets.ModelViewSet):
    queryset = DeviceType.objects.all()
    serializer_class = DeviceTypeSerializer


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


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
