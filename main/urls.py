from django.urls import include, path
from rest_framework_nested import routers
from .views import (
    GuestViewSet,
    FloorViewSet,
    RoomTypeViewSet,
    RoomViewSet,
    AmenityViewSet,
    ReservationViewSet,
    InstallmentViewSet,
    PaymentViewSet,
    ReviewViewSet,
)

app_name = "main"


router = routers.DefaultRouter()

router.register("guests", GuestViewSet)
router.register("floors", FloorViewSet)


router.register("room", RoomViewSet)
room_router = routers.NestedDefaultRouter(router, "room", lookup="room")
room_router.register("reviews", ReviewViewSet, basename="room-reviews")
room_router.register("amenities", AmenityViewSet, basename="room-amenities")

router.register("room-types", RoomTypeViewSet)
room_type_router = routers.NestedDefaultRouter(router, "room-types", lookup="room_type")
room_type_router.register("rooms", RoomViewSet, basename="room-type-rooms")

urlpatterns = router.urls + room_router.urls + room_type_router.urls
