from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from main.models import Installment


@receiver([post_save, post_delete], sender=Installment)
def update_reservation_payment_status(sender, instance, **kwargs):
    reservation = instance.reservation
    reservation.save()
