from django.urls import include, path
from rest_framework_nested import routers
from .views import (
    GuestViewSet,
    FloorViewSet,
    RoomTypeViewSet,
    RoomViewSet,
    RoomImageViewSet,
    RoomAmenityViewSet,
    ReservationViewSet,
    InstallmentViewSet,
    PaymentViewSet,
    RefundViewSet,
    ReviewViewSet,
)

app_name = "main"


router = routers.DefaultRouter()

# guests
router.register("guests", GuestViewSet)

# room_types
router.register("room-types", RoomTypeViewSet)

# floors/<id>/rooms/<id>
router.register("floors", FloorViewSet)
floor_router = routers.NestedSimpleRouter(router, "floors", lookup="floor")
# floors/<id>/rooms
floor_router.register("rooms", RoomViewSet, basename="floor-rooms")


router.register("rooms", RoomViewSet)
room_router = routers.NestedDefaultRouter(router, "rooms", lookup="rooms")
# room/<id>/reviews
room_router.register("reviews", ReviewViewSet, basename="room-reviews")
# room/<id>/amenities
room_router.register("amenities", RoomAmenityViewSet, basename="room-amenities")
# room/<id>/images
room_router.register("images", RoomImageViewSet, basename="room-images")

# reservations
router.register("reservations", ReservationViewSet)

# installments
router.register("installments", InstallmentViewSet)

# payments
router.register("payments", PaymentViewSet)

# reservations/<id>/installments/<id>/payments/<id>
# http://127.0.0.1:8000/api/reservations/66/installments/32/payments/7/

# Create a nested router for installments
installment_router = routers.NestedDefaultRouter(
    router, "reservations", lookup="reservation"
)
installment_router.register(
    "installments", InstallmentViewSet, basename="reservation-installments"
)


# Create a nested router for payments
payment_router = routers.NestedDefaultRouter(
    installment_router, "installments", lookup="installment"
)


payment_router.register("payments", PaymentViewSet, basename="installment-payments")


# refunds
router.register("refunds", RefundViewSet)

urlpatterns = (
    router.urls
    + room_router.urls
    + floor_router.urls
    + installment_router.urls
    + payment_router.urls
)
