from rest_framework.serializers import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from .models import (
    Guest,
    Floor,
    RoomType,
    Room,
    RoomImage,
    Amenity,
    Reservation,
    Installment,
    Payment,
    Refund,
    Review,
)

from user.serializers import UserSerializer


class GuestSerializer(ModelSerializer):
    user = UserSerializer(read_only=True, required=False)

    class Meta:
        model = Guest
        fields = ["id", "user", "image", "contact_info", "nid", "preferences", "status"]


class FloorSerializer(ModelSerializer):
    class Meta:
        model = Floor
        fields = ["id", "level", "description"]


class RoomTypeSerializer(ModelSerializer):
    class Meta:
        model = RoomType
        fields = ["id", "room_type", "price", "description"]


class RoomImageSerializer(ModelSerializer):

    def create(self, validated_data):
        room_id = self.context["room_id"]
        return RoomImage.objects.create(room_id=room_id, **validated_data)

    class Meta:
        model = RoomImage
        fields = ["id", "room", "image", "alt_text"]


class RoomSerializer(ModelSerializer):
    room_type = RoomTypeSerializer(read_only=True, required=False)
    images = RoomImageSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = [
            "id",
            "floor",
            "room_label",
            "room_type",
            "capacity",
            "description",
            "availability",
            "images",
        ]


class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = [
            "id",
            "room",
            "title",
            "description",
            "availability",
        ]


class ReservationSerializer(ModelSerializer):
    class Meta:
        model = Reservation
        fields = [
            "id",
            "room",
            "user",
            "start_date",
            "end_date",
            "reservation_status",
        ]


class InstallmentSerializer(ModelSerializer):
    reservation = SerializerMethodField(method_name="get_reservation")

    class Meta:
        model = Installment
        fields = [
            "id",
            "reservation",
            "installment_type",
            "installment_amount",
        ]

    def create(self, validated_data):
        reservation_id = self.context["reservation_id"]
        return Installment.objects.create(
            reservation_id=reservation_id, **validated_data
        )

    def get_reservation(self, obj):
        return obj.reservation.id


class PaymentSerializer(ModelSerializer):
    installment = SerializerMethodField(method_name="get_installment")

    class Meta:
        model = Payment
        fields = [
            "id",
            "payment_id",
            "installment",
            "payment_amount",
            "payment_method",
        ]

    def create(self, validated_data):
        installment_id = self.context["installment_id"]
        return Payment.objects.create(installment_id=installment_id, **validated_data)

    def get_installment(self, obj):
        return obj.installment.id


class RefundSerializer(ModelSerializer):
    class Meta:
        model = Refund
        fields = [
            "id",
            "payment",
            "refund_amount",
            "refund_date",
            "refund_method",
        ]


class ReviewSerializer(ModelSerializer):
    guest = SerializerMethodField()

    class Meta:
        model = Review
        fields = ["id", "guest", "rating", "comment", "images", "likes"]

    def create(self, validated_data):
        room_id = self.context["room_id"]
        guest = self.context["guest"]
        return Review.objects.create(room_id=room_id, guest=guest, **validated_data)

    def get_guest(self, obj):
        return obj.guest.user.username
