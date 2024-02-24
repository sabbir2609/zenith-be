from django_filters.rest_framework import FilterSet
from main.models import Room


class RoomFilter(FilterSet):
    class Meta:
        model = Room
        fields = {
            "floor": ["exact"],
            "room_type": ["exact"],
            "room_type__price": ["exact", "lt", "gt"],
            "is_available": ["exact"],
            "capacity": ["exact", "lt", "gt"],
        }
