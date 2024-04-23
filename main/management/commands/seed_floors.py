from django.core.management.base import BaseCommand
from main.models import Floor
from django.utils.translation import gettext_lazy as _


class Command(BaseCommand):
    help = _("Seeds the database with initial floor levels and descriptions")

    def handle(self, *args, **kwargs):
        floors = [
            {"level": 1, "description": _("Ground floor with lobby and common areas.")},
            {
                "level": 2,
                "description": _(
                    "Standard rooms, laundry facilities, and vending machines."
                ),
            },
            {"level": 3, "description": _("Deluxe rooms with business services.")},
            {"level": 4, "description": _("Executive suites and meeting rooms.")},
            {"level": 5, "description": _("Family-friendly floor with play areas.")},
            {"level": 10, "description": _("Premium suites with panoramic views.")},
            {"level": 15, "description": _("Executive suites with private amenities.")},
            {"level": 20, "description": _("Penthouse and luxury accommodations.")},
        ]

        for floor in floors:
            if not Floor.objects.filter(level=floor["level"]).exists():
                Floor.objects.create(**floor)

        self.stdout.write(self.style.SUCCESS(_("Successfully seeded floors")))
