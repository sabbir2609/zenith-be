from rest_framework_nested import routers
from .views import (
    FacilityViewSet,
    FacilityAmenitiesViewSet,
    FacilityImageViewSet,
    FacilityReviewViewSet,
    FacilityReviewListViewSet,
    FacilityReservationViewSet,
    InstallmentViewSet,
    PaymentViewSet,
    RefundViewSet,
)


app_name = "facility"

router = routers.DefaultRouter()

# Routers for the root level
router.register("facilities", FacilityViewSet, basename="facility")
router.register("amenities", FacilityAmenitiesViewSet, basename="amenities")
router.register("images", FacilityImageViewSet, basename="images")
router.register("reviews", FacilityReviewListViewSet, basename="reviews")
router.register(
    "reservations",
    FacilityReservationViewSet,
    basename="reservations",
)
router.register("installments", InstallmentViewSet, basename="installment")
router.register("payments", PaymentViewSet, basename="payment")
router.register("refunds", RefundViewSet, basename="refund")

# Routers for nested level
facilities_router = routers.NestedDefaultRouter(router, "facilities", lookup="facility")
facilities_router.register(
    "amenities", FacilityAmenitiesViewSet, basename="facility-amenities"
)
facilities_router.register("images", FacilityImageViewSet, basename="facility-images")
facilities_router.register(
    "reviews", FacilityReviewViewSet, basename="facility-reviews"
)
facilities_router.register(
    "reservations", FacilityReservationViewSet, basename="facility-reservations"
)


urlpatterns = router.urls + facilities_router.urls
