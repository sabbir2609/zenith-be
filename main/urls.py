from rest_framework.routers import DefaultRouter
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

router = DefaultRouter()

router.register(r"guests", GuestViewSet, basename="guest")
router.register(r"floors", FloorViewSet, basename="floor")
router.register(r"room-types", RoomTypeViewSet, basename="roomtype")
router.register(r"rooms", RoomViewSet, basename="room")
router.register(r"amenities", AmenityViewSet, basename="amenity")
router.register(r"reservations", ReservationViewSet, basename="reservation")
router.register(r"installments", InstallmentViewSet, basename="installment")
router.register(r"payments", PaymentViewSet, basename="payment")
router.register(r"reviews", ReviewViewSet, basename="review")

urlpatterns = router.urls
