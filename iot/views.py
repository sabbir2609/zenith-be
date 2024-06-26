from django.views.generic import TemplateView

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from iot.pagination import DefaultPagination
from iot.models import DeviceType, Device, RoomDevice, FacilityDevice
from iot.serializers import (
    DeviceTypeSerializer,
    DeviceSerializer,
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
    serializer_class = DeviceSerializer
    pagination_class = DefaultPagination
    search_fields = ["name", "client_id", "topic"]
    ordering_fields = ["installation_date", "status", "qos", "created_at"]

    def get_serializer_class(self):
        if self.action == "list":
            return DeviceListSerializer
        if self.action == "retrieve":
            return DeviceDetailSerializer
        return super().get_serializer_class()

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data["active_devices_count"] = Device.objects.filter(
            status=True
        ).count()
        return response

    @action(detail=False, methods=["get"])
    def qos_choices(self, request):
        qos_choices = Device.QosChoices.choices
        qos_choices = [{"id": id, "name": name} for id, name in qos_choices]
        return Response(qos_choices)


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
