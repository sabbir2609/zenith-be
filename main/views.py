from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from main.permissions import (
    IsAdminUserOrReadOnly,
    IsAdminOrStaffUserOrReadOnly,
    IsReservationOwnerOrAdmin,
)

from main.models import (
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
from main.serializers import (
    GuestSerializer,
    FloorSerializer,
    RoomTypeSerializer,
    RoomSerializer,
    AmenitySerializer,
    ReservationSerializer,
    InstallmentSerializer,
    PaymentSerializer,
    ReviewSerializer,
    RefundSerializer,
)


class GuestViewSet(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    permission_classes = [IsAdminUser]


class FloorViewSet(viewsets.ModelViewSet):
    queryset = Floor.objects.all()
    serializer_class = FloorSerializer
    permission_classes = [IsAdminUserOrReadOnly]


class RoomTypeViewSet(viewsets.ModelViewSet):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer
    permission_class = [IsAdminUserOrReadOnly]


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAdminUserOrReadOnly]


class AmenityViewSet(viewsets.ModelViewSet):
    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer
    permission_classes = [IsAdminOrStaffUserOrReadOnly]


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsReservationOwnerOrAdmin]

    def get_serializer_context(self):
        return {"user": self.request.user}


class InstallmentViewSet(viewsets.ModelViewSet):
    queryset = Installment.objects.all()
    serializer_class = InstallmentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class RefundViewSet(viewsets.ModelViewSet):
    queryset = Refund.objects.all()
    serializer_class = RefundSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(room_id=self.kwargs["room_pk"])

    def get_serializer_context(self):
        user = self.request.user
        guest = Guest.objects.filter(user=user).first()

        return {"room_id": self.kwargs.get("room_pk"), "guest": guest}
