from encodings.punycode import T
import random
import string
from django.core.management.base import BaseCommand
from faker import Faker

from users.models import User

fake = Faker()

class Command(BaseCommand):
    help = 'Generate dummy user accounts'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Number of users to create')

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        users_created = 0

        for _ in range(count):
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = fake.user_name()
            email = fake.email()
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

            if not User.objects.filter(username=username).exists():
                User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    email=email,
                    password=password
                )
                users_created += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully created {users_created} users'))
