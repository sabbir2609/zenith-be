from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from django.db import transaction
from faker import Faker
from main.models import Floor, RoomType, Room
from django.db import IntegrityError


class Command(BaseCommand):
    help = "Creates random devices and topics"

    def add_arguments(self, parser):
        parser.add_argument(
            "n", type=int, help="Indicates the number of devices to be created"
        )

    def handle(self, *args, **kwargs):
        n = kwargs["n"]
        fake = Faker()

        def generate_room_name():
            return get_random_string(length=1, allowed_chars="ABCDEFGHIJ")

        @transaction.atomic
        def create_fake_data(n):
            self.stdout.write("Starting to generate data...")
            for _ in range(n):
                floor = Floor.objects.order_by("?").first()
                room_type = RoomType.objects.order_by("?").first()
                capacity = fake.random_int(min=1, max=10)
                description = fake.text(max_nb_chars=200, ext_word_list=None)
                is_available = fake.boolean(chance_of_getting_true=50)

                room_created = False
                while not room_created:
                    try:
                        room_label = generate_room_name()
                        room = Room.objects.create(
                            floor=floor,
                            room_label=room_label,
                            room_type=room_type,
                            capacity=capacity,
                            description=description,
                            is_available=is_available,
                        )
                        room_created = True
                    except IntegrityError:
                        continue

                self.stdout.write(
                    f"Created room {room.room_label} in floor {room.floor.level}"
                )

            self.stdout.write("Data generation completed.")

        create_fake_data(n)
