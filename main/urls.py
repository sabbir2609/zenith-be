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

# floors/<id>/rooms/<id>
router.register("floors", FloorViewSet)
floor_router = routers.NestedDefaultRouter(router, "floors", lookup="floor")
floor_router.register("rooms", RoomViewSet, basename="floor-rooms")

# room/reviews
# room/amenities
router.register("room", RoomViewSet)
room_router = routers.NestedDefaultRouter(router, "room", lookup="room")
room_router.register("reviews", ReviewViewSet, basename="room-reviews")
room_router.register("amenities", AmenityViewSet, basename="room-amenities")

# reservations
router.register("reservations", ReservationViewSet)
# installments
router.register("installments", InstallmentViewSet)
# payments
router.register("payments", PaymentViewSet)


urlpatterns = router.urls + room_router.urls + floor_router.urls
