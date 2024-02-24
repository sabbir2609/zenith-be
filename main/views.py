from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from main.permissions import (
    IsAdminOrInstallmentOwner,
    IsAdminOrReservationOwner,
    IsAdminUserOrReadOnly,
    IsAdminOrStaffUserOrReadOnly,
    IsAdminOrOwner,
)

from main.models import (
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
from main.serializers import (
    GuestSerializer,
    FloorSerializer,
    RoomTypeSerializer,
    RoomSerializer,
    RoomImageSerializer,
    AmenitySerializer,
    ReservationSerializer,
    InstallmentSerializer,
    PaymentSerializer,
    ReviewSerializer,
    RefundSerializer,
)


class GuestViewSet(ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    permission_classes = [IsAdminUser]


class FloorViewSet(ModelViewSet):
    queryset = Floor.objects.all()
    serializer_class = FloorSerializer
    permission_classes = [IsAdminUserOrReadOnly]


class RoomTypeViewSet(ModelViewSet):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer
    permission_class = [IsAdminUserOrReadOnly]


class RoomViewSet(ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAdminUserOrReadOnly]


class RoomImageViewSet(ModelViewSet):
    queryset = RoomImage.objects.all()
    serializer_class = RoomImageSerializer
    permission_classes = [IsAdminOrStaffUserOrReadOnly]

    def get_queryset(self):
        return RoomImage.objects.filter(room_id=self.kwargs["room_pk"])

    def get_serializer_context(self):
        return {"room_id": self.kwargs.get("room_pk")}


class AmenityViewSet(ModelViewSet):
    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer
    permission_classes = [IsAdminOrStaffUserOrReadOnly]


class ReservationViewSet(ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAdminOrOwner()]
        elif self.action == "create":
            return [IsAuthenticated()]
        elif self.action in ["retrieve", "list"]:
            return [IsAdminOrOwner()]
        else:
            return [IsAdminUser()]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_staff or user.is_superuser:
                return Reservation.objects.all()
            else:
                return Reservation.objects.select_related("room", "user").filter(
                    user=user
                )
        else:
            return Reservation.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class InstallmentViewSet(ModelViewSet):
    queryset = Installment.objects.all()
    serializer_class = InstallmentSerializer

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAdminOrReservationOwner()]
        elif self.action == "create":
            return [IsAuthenticated()]
        elif self.action in ["retrieve", "list"]:
            return [IsAdminOrReservationOwner()]
        else:
            return [IsAdminUser()]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_staff or user.is_superuser:
                return Installment.objects.all()
            else:
                return Installment.objects.filter(
                    reservation=self.kwargs["reservation_pk"]
                )
        else:
            return Installment.objects.none()

    def get_serializer_context(self):
        return {"reservation_id": self.kwargs.get("reservation_pk")}


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAdminOrInstallmentOwner()]
        elif self.action == "create":
            return [IsAuthenticated()]
        elif self.action in ["retrieve", "list"]:
            return [IsAdminOrInstallmentOwner()]
        else:
            return [IsAdminUser()]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_staff or user.is_superuser:
                return Payment.objects.all()
            else:
                return Payment.objects.filter(installment=self.kwargs["installment_pk"])
        else:
            return Payment.objects.none()

    def get_serializer_context(self):
        return {"installment_id": self.kwargs.get("installment_pk")}


class RefundViewSet(ModelViewSet):
    queryset = Refund.objects.all()
    serializer_class = RefundSerializer


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(room_id=self.kwargs["room_pk"])

    def get_serializer_context(self):
        user = self.request.user
        guest = Guest.objects.filter(user=user).first()

        return {"room_id": self.kwargs.get("room_pk"), "guest": guest}
