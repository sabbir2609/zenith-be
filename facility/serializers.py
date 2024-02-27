from rest_framework.serializers import ModelSerializer
from .models import (
    Facility,
    FacilityAmenities,
    FacilityImage,
    FacilityReview,
    FacilityReservation,
    Installment,
    Payment,
    Refund,
)


class FacilitySerializer(ModelSerializer):
    class Meta:
        model = Facility
        fields = "__all__"


class FacilityAmenitiesSerializer(ModelSerializer):
    class Meta:
        model = FacilityAmenities
        fields = "__all__"


class FacilityImageSerializer(ModelSerializer):
    class Meta:
        model = FacilityImage
        fields = "__all__"


class FacilityReviewSerializer(ModelSerializer):
    class Meta:
        model = FacilityReview
        fields = "__all__"


class FacilityReservationSerializer(ModelSerializer):
    class Meta:
        model = FacilityReservation
        fields = "__all__"


class InstallmentSerializer(ModelSerializer):
    class Meta:
        model = Installment
        fields = "__all__"


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class RefundSerializer(ModelSerializer):
    class Meta:
        model = Refund
        fields = "__all__"
