import datetime
from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import (
    Facility,
    FacilityAmenities,
    FacilityImage,
    FacilityReview,
    FacilityExtraCharge,
    FacilityReservation,
)


class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = "__all__"


class FacilityExtraChargeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacilityExtraCharge
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


class FacilityReservationAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacilityReservation
        fields = [
            "id",
            "facility",
            "user",
            "date",
            "start_time",
            "end_time",
            "number_of_people",
            "total_amount",
        ]
        read_only_fields = ["total_amount"]


class FacilityReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacilityReservation
        fields = [
            "id",
            "facility",
            "user",
            "date",
            "start_time",
            "end_time",
            "number_of_people",
            "total_amount",
        ]

    def validate(self, data):
        errors = {}
        if data["date"] < datetime.datetime.now().date():
            errors["date"] = "Reservation date cannot be in the past."
        if data["start_time"] < data["facility"].opening_time:
            errors["start_time"] = (
                "Reservation start date cannot be before facility opening time."
            )
        if data["end_time"] > data["facility"].closing_time:
            errors["end_time"] = (
                "Reservation end date cannot be after facility closing time."
            )

        overlapping_reservations = FacilityReservation.objects.filter(
            facility=data["facility"],
            date=data["date"],
            start_time__lt=data["end_time"],
            end_time__gt=data["start_time"],
        )

        if overlapping_reservations.exists():
            errors["overlapping"] = (
                "A reservation already exists at the selected date and time range."
            )

        if errors:
            raise serializers.ValidationError(errors)

        return data
