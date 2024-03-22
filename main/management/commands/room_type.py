from django.core.management.base import BaseCommand
from main.models import RoomType


room_types = [
    {
        "name": "Standard Single Room",
        "description": "A comfortable room with essential amenities, suitable for single occupancy.",
        "base_price": 80.00,
    },
    {
        "name": "Standard Double Room",
        "description": "A comfortable room with essential amenities, suitable for double occupancy.",
        "base_price": 100.00,
    },
    {
        "name": "Deluxe King Room",
        "description": "A spacious room with a king-size bed and additional amenities.",
        "base_price": 150.00,
    },
    {
        "name": "Executive Suite",
        "description": "A luxurious suite with separate living and sleeping areas, perfect for business travelers.",
        "base_price": 250.00,
    },
    {
        "name": "Family Room",
        "description": "A large room suitable for families, with multiple beds and amenities for children.",
        "base_price": 180.00,
    },
    {
        "name": "Ocean View Room",
        "description": "A room with a beautiful view of the ocean, providing a serene environment for relaxation.",
        "base_price": 200.00,
    },
    {
        "name": "Presidential Suite",
        "description": "The most luxurious suite in the hotel, offering unparalleled comfort and amenities.",
        "base_price": 500.00,
    },
    {
        "name": "Accessible Room",
        "description": "A specially designed room with accessibility features for guests with disabilities.",
        "base_price": 120.00,
    },
    {
        "name": "Honeymoon Suite",
        "description": "A romantic suite perfect for honeymooners, with special amenities for couples.",
        "base_price": 300.00,
    },
    {
        "name": "Penthouse Apartment",
        "description": "An exclusive penthouse offering breathtaking views and luxurious living spaces.",
        "base_price": 800.00,
    },
]


class Command(BaseCommand):
    help = "Create room types"

    def handle(self, *args, **kwargs):
        for room_type in room_types:
            RoomType.objects.create(
                room_type=room_type["name"],
                description=room_type["description"],
                price=room_type["base_price"],
            )

        self.stdout.write(self.style.SUCCESS("Room types created successfully"))
