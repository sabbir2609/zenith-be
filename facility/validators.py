# Facility Reservation validators

from django.core.exceptions import ValidationError
from datetime import datetime


def validate_reservation_date(value):
    if value < datetime.now().date():
        raise ValidationError("Reservation date cannot be in the past.")
