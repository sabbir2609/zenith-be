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
    Refund,
    Review,
)


class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = "__all__"


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
        fields = [
            "id",
            "room",
            "title",
            "description",
            "availability",
        ]


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = [
            "id",
            "room",
            "start_date",
            "end_date",
            "reservation_status",
        ]


class InstallmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Installment
        fields = [
            "id",
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
            "payment_amount",
            "payment_date",
            "payment_method",
        ]


class RefundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refund
        fields = [
            "id",
            "payment",
            "refund_amount",
            "refund_date",
            "refund_method",
        ]


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "rating", "comment", "images"]

    def create(self, validated_data):
        room_id = self.context["room_id"]
        guest = self.context["guest"]
        return Review.objects.create(room_id=room_id, guest=guest, **validated_data)
