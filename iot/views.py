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

from iot.mqtt.client import client as mqtt_client


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

        topic = Device.objects.get(client_id=self.kwargs["device_id"]).topic
        mqtt_client.subscribe(topic)

        from asgiref.sync import async_to_sync
        from channels.layers import get_channel_layer

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'{context["device_id"]}',
            {
                "type": "on_message",
                "message": f"{mqtt_client.on_message}",
            },
        )

        context["title"] = "IoT Devices Websocket Test"
        context["device_id"] = self.kwargs["device_id"]
        return context
