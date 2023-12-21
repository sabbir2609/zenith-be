from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist

from main.models import Installment, Reservation, Guest


@receiver(post_save, sender=Reservation)
def create_and_update_guest(sender, instance, created, **kwargs):
    if created:
        # Create a Guest instance for the user
        guest, _ = Guest.objects.get_or_create(user=instance.user)

        # Associate the Guest instance with the reservation
        instance.guest = guest
        instance.save()

    # Update the guest status based on the reservation status
    if instance.reservation_status == Reservation.ReservationStatusChoices.CHECKED_IN:
        instance.guest.status = True
    else:
        instance.guest.status = False

    instance.guest.save()
