from rest_framework import serializers
from django.core.exceptions import ValidationError
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


class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = "__all__"


class FacilityAmenitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacilityAmenities
        fields = "__all__"


class FacilityImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacilityImage
        fields = "__all__"


class FacilityReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacilityReview
        fields = ["description", "rating"]

    def create(self, validated_data):
        facility_id = self.context["facility_id"]
        user = self.context["user"]

        return FacilityReview.objects.create(
            facility_id=facility_id, reviewer=user, **validated_data
        )

    def get_user_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"


class FacilityReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacilityReview
        fields = ["id", "reviewer", "facility", "description", "rating", "created_at"]


class FacilityReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacilityReservation
        fields = "__all__"


class FacilityReservationAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacilityReservation
        fields = ["facility", "user", "date", "start_time", "end_time"]

    def validate(self, data):
        facility = data["facility"]
        date = data["date"]
        start_time = data["start_time"]
        end_time = data["end_time"]

        if not facility.is_reservable:
            raise serializers.ValidationError(
                {"error": "This facility is not reservable"}
            )

        overlapping_reservations = FacilityReservation.objects.filter(
            facility=facility,
            date=date,
            start_time__lt=end_time,
            end_time__gt=start_time,
        )
        if overlapping_reservations.exists():
            raise serializers.ValidationError(
                {
                    "error": "This facility is already reserved for the given date and time"
                }
            )

        return data


class FacilityReservationUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacilityReservation
        fields = ["date", "start_time", "end_time"]

    def create(self, validated_data):
        user = self.context["user"]
        facility_id = self.context["facility_id"]
        return FacilityReservation.objects.create(
            user=user, facility_id=facility_id, **validated_data
        )

    def validate(self, data):
        facility_id = self.context["facility_id"]
        date = data["date"]
        start_time = data["start_time"]
        end_time = data["end_time"]

        facility = Facility.objects.get(id=facility_id)
        if not facility.is_reservable:
            raise serializers.ValidationError(
                {"error": "This facility is not reservable"}
            )

        overlapping_reservations = FacilityReservation.objects.filter(
            facility=facility,
            date=date,
            start_time__lt=end_time,
            end_time__gt=start_time,
        )
        if overlapping_reservations.exists():
            raise serializers.ValidationError(
                {
                    "error": "This facility is already reserved for the given date and time"
                }
            )

        return data


class InstallmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Installment
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class RefundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refund
        fields = "__all__"
