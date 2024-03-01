from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import (
    Facility,
    FacilityAmenities,
    FacilityImage,
    FacilityReview,
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
