from django.urls import path
from rest_framework_nested import routers
from iot.views import (
    DeviceTypeViewSet,
    DeviceViewSet,
    RoomDeviceViewSet,
    FacilityDeviceViewSet,
    IoTChannel,
)

app_name = "iot"

router = routers.DefaultRouter()
# device types router
router.register("device-types", DeviceTypeViewSet, basename="device-types")

# devices router
router.register("devices", DeviceViewSet, basename="devices")

# room device router
router.register("room-devices", RoomDeviceViewSet, basename="rooms")

# facility device router
router.register("facility-devices", FacilityDeviceViewSet, basename="facilities")

urlpatterns = [
    path("ws/<str:device_id>/", IoTChannel.as_view(), name="channels"),
] + router.urls
