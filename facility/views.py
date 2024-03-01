from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from management.permissions import IsManager, IsReceptionist, IsHousekeeping

from .models import (
    Facility,
    FacilityAmenities,
    FacilityImage,
    FacilityReview,
)
from .serializers import (
    FacilitySerializer,
    FacilityAmenitiesSerializer,
    FacilityImageSerializer,
    FacilityReviewSerializer,
    FacilityReviewListSerializer,
)


class FacilityViewSet(viewsets.ModelViewSet):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsAdminUser(), IsManager()]
        elif self.action == "create":
            return [IsAdminUser(), IsManager()]
        elif self.action in ["retrieve", "list", "reservable_facilities"]:
            return [AllowAny()]
        else:
            return [IsAuthenticated(), IsAdminUser()]

    # action to see all reservable facilities
    @action(detail=False, methods=["get"], url_path="reservable", url_name="reservable")
    def reservable_facilities(self, request, *args, **kwargs):
        queryset = Facility.objects.filter(is_reservable=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class FacilityAmenitiesViewSet(viewsets.ModelViewSet):
    queryset = FacilityAmenities.objects.all()
    serializer_class = FacilityAmenitiesSerializer

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsAdminUser(), IsManager()]
        elif self.action == "create":
            return [IsAdminUser(), IsManager()]
        elif self.action in ["retrieve", "list"]:
            return [AllowAny()]
        else:
            return [IsAuthenticated(), IsAdminUser()]


class FacilityImageViewSet(viewsets.ModelViewSet):
    queryset = FacilityImage.objects.all()
    serializer_class = FacilityImageSerializer

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsAdminUser(), IsManager()]
        elif self.action == "create":
            return [IsAdminUser(), IsManager()]
        elif self.action in ["retrieve", "list"]:
            return [AllowAny()]
        else:
            return [IsAuthenticated(), IsAdminUser()]


class FacilityReviewViewSet(viewsets.ModelViewSet):
    queryset = FacilityReview.objects.all()
    serializer_class = FacilityReviewSerializer

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthenticated()]
        elif self.action == "create":
            return [IsAuthenticated()]
        elif self.action in ["retrieve", "list"]:
            return [AllowAny()]
        else:
            return [IsAuthenticated()]


class FacilityReviewListViewSet(viewsets.ModelViewSet):
    queryset = FacilityReview.objects.all()
    serializer_class = FacilityReviewListSerializer

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthenticated()]
        elif self.action == "create":
            return [IsAuthenticated()]
        elif self.action in ["retrieve", "list"]:
            return [AllowAny()]
        else:
            return [IsAuthenticated()]


class FacilityReviewViewSet(viewsets.ModelViewSet):
    serializer_class = FacilityReviewSerializer

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthenticated()]
        elif self.action == "create":
            return [IsAuthenticated()]
        elif self.action in ["retrieve", "list"]:
            return [AllowAny()]
        else:
            return [IsAuthenticated()]

    def get_queryset(self):
        facility_id = self.kwargs.get("facility_pk")
        if facility_id:
            return FacilityReview.objects.filter(facility=facility_id)
        return FacilityReview.objects.all()

    def get_serializer_context(self):
        return {
            "facility_id": self.kwargs.get("facility_pk"),
            "user": self.request.user,
        }
