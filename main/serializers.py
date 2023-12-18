from rest_framework import serializers
from .models import (
    Guest,
    Floor,
    RoomType,
    Room,
    Amenity,
    Reservation,
    Installment,
    Payment,
    Review,
)


class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = ["id", "user", "name", "contact_info", "preferences"]


class FloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Floor
        fields = ["id", "level", "description"]


class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = ["id", "room_type", "price", "description"]


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = [
            "id",
            "floor",
            "room_label",
            "room_type",
            "capacity",
            "images",
            "description",
            "availability",
        ]


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ["id", "room", "title", "description", "availability"]


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = [
            "id",
            "guest",
            "room",
            "start_date",
            "end_date",
            "reservation_status",
            "payment_status",
        ]


class InstallmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Installment
        fields = [
            "id",
            "installment_id",
            "installment_type",
            "reservation",
            "installment_date",
            "installment_amount",
        ]


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "payment_id",
            "installment",
            "amount",
            "payment_date",
            "payment_method",
        ]


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "rating", "comment", "images"]

    def create(self, validated_data):
        room_id = self.context["room_id"]
        return Review.objects.create(room_id=room_id, **validated_data)
