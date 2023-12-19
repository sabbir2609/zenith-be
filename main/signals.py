from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist


from main.models import Installment, Reservation, Guest


@receiver([post_save, post_delete], sender=Installment)
def update_reservation_payment_status(sender, instance, **kwargs):
    reservation = instance.reservation
    reservation.save()


# Signal receiver function to create or update Guest profile
@receiver(post_save, sender=Reservation)
def create_or_update_guest_profile(sender, instance, created, **kwargs):
    if created:
        # Check if the guest already exists for the user
        try:
            guest = Guest.objects.get(user=instance.user)
        except ObjectDoesNotExist:
            # If the guest does not exist, create a new guest
            guest = Guest.objects.create(
                user=instance.user,
                contact_info=instance.contact_info,
                nid=instance.nid,
            )

        # Update Guest information based on the reservation
        guest.contact_info = instance.contact_info or guest.contact_info
        guest.nid = instance.nid or guest.nid
        guest.save()

        # Assign the guest to the reservation
        instance.guest = guest
        instance.save()
