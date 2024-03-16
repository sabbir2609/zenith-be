from django.core.management.base import BaseCommand
from faker import Faker
from iot.models import Device, Topic, DeviceType
from django.db import transaction
import random
import string


class Command(BaseCommand):
    help = "Creates random devices and topics"

    def add_arguments(self, parser):
        parser.add_argument(
            "n", type=int, help="Indicates the number of devices to be created"
        )

    def handle(self, *args, **kwargs):
        n = kwargs["n"]
        fake = Faker()

        device_types = [
            "Smart Light",
            "Smart Bulbs",
            "Smart Switches and Dimmers",
            "Smart Light Strips",
            "Smart Light Panels",
            "Smart TV",
            "Smart Thermostat",
            "Smart AC",
        ]

        def generate_device_name(device_type):
            return f"{device_type} {fake.random_int(min=1, max=100)}"

        def generate_random_topic(levels=3, max_length=10):
            topic = ""
            for _ in range(levels):
                topic += "".join(
                    random.choices(
                        string.ascii_lowercase, k=random.randint(1, max_length)
                    )
                )
                topic += "/"
            return topic[:-1]

        def generate_client_id():
            return f"{fake.random_uppercase_letter()}{fake.random_uppercase_letter()}{fake.random_uppercase_letter()}{fake.random_number(digits=4)}"

        @transaction.atomic
        def create_fake_data(n):
            self.stdout.write("Starting to generate data...")
            for _ in range(n):
                device_type, created = DeviceType.objects.get_or_create(
                    name=random.choice(device_types)
                )
                device = Device.objects.create(
                    name=generate_device_name(device_type),
                    device_type=device_type,
                    client_id=generate_client_id(),
                    qos=fake.random_int(min=0, max=3),
                    status=fake.boolean(),
                    description=fake.text(),
                    installation_date=fake.date_between(
                        start_date="-1y", end_date="today"
                    ),
                )
                Topic.objects.create(
                    device=device,
                    name=generate_random_topic(),
                    description=fake.text(),
                )
            self.stdout.write("Finished generating data.")

        create_fake_data(n)
