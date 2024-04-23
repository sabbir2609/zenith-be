from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from main.pagination import DefaultPagination

from main.filters import RoomFilter

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
    RoomAmenity,
    Reservation,
    Installment,
    Payment,
    Refund,
    Review,
    ReviewImage,
)
from main.serializers import (
    GuestSerializer,
    FloorSerializer,
    RoomTypeSerializer,
    RoomSerializer,
    RoomImageSerializer,
    RoomAmenitySerializer,
    ReservationSerializer,
    InstallmentSerializer,
    PaymentSerializer,
    ReviewSerializer,
    ReviewImageSerializer,
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
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = RoomFilter
    pagination_class = DefaultPagination
    ordering_fields = ["id"]

    search_fields = [
        "description",
        "floor__level",
        "room_type__room_type",
        "room_type__description",
        "room_type__price",
    ]

    @action(detail=False, methods=["get"])
    def available(self, request):
        start_date = request.query_params.get("start_date", None)
        end_date = request.query_params.get("end_date", None)

        if start_date is None or end_date is None:
            return Response(
                {"error": "Both start_date and end_date are required"}, status=400
            )

        rooms = Room.objects.filter(
            ~Q(
                reservations__start_date__lt=end_date,
                reservations__end_date__gt=start_date,
            )
        )

        serializer = self.get_serializer(rooms, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        floor_id = self.kwargs.get("floor_pk", None)
        if floor_id is not None:
            return Room.objects.filter(floor__id=floor_id)
        else:
            return Room.objects.all()

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data["available_rooms_count"] = Room.objects.filter(
            is_available=True
        ).count()

        return response


class RoomImageViewSet(ModelViewSet):
    queryset = RoomImage.objects.all()
    serializer_class = RoomImageSerializer
    permission_classes = [IsAdminOrStaffUserOrReadOnly]

    def get_queryset(self):
        return RoomImage.objects.filter(room_id=self.kwargs["room_pk"])

    def get_serializer_context(self):
        return {"room_id": self.kwargs.get("room_pk")}


class RoomAmenityViewSet(ModelViewSet):
    queryset = RoomAmenity.objects.all()
    serializer_class = RoomAmenitySerializer
    permission_classes = [IsAdminOrStaffUserOrReadOnly]

    def get_queryset(self):
        return RoomAmenity.objects.filter(room_id=self.kwargs["room_pk"])

    def get_serializer_context(self):
        return {"room_id": self.kwargs.get("room_pk")}


class ReservationViewSet(ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsAdminOrOwner()]
        elif self.action == "create":
            return [IsAuthenticated()]
        elif self.action in ["retrieve", "list"]:
            return [IsAuthenticated(), IsAdminOrOwner()]
        else:
            return [IsAuthenticated(), IsAdminUser()]

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
            return [IsAuthenticated(), IsAdminOrReservationOwner()]
        elif self.action == "create":
            return [IsAuthenticated(), IsAdminOrReservationOwner()]
        elif self.action in ["retrieve", "list"]:
            return [IsAuthenticated(), IsAdminOrReservationOwner()]
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
            return [IsAuthenticated(), IsAdminOrInstallmentOwner()]
        elif self.action == "create":
            return [IsAuthenticated(), IsAuthenticated()]
        elif self.action in ["retrieve", "list"]:
            return [IsAuthenticated(), IsAdminOrInstallmentOwner()]
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


class ReviewImageViewSet(ModelViewSet):
    queryset = ReviewImage.objects.all()
    serializer_class = ReviewImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ReviewImage.objects.filter(review_id=self.kwargs["review_pk"])

    def get_serializer_context(self):
        return {"review_id": self.kwargs.get("review_pk")}
