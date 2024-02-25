from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from main.models import Installment, Payment, Refund, Reservation, Guest


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


@receiver(post_save, sender=Payment)
def update_installment_status(sender, instance, **kwargs):
    instance.installment.installment_status = (
        "Paid"
        if instance.payment_amount >= instance.installment.installment_amount
        else "Pending"
    )
    instance.installment.save()


@receiver(post_save, sender=Payment)
@receiver(post_delete, sender=Payment)
def update_reservation_payment_status(sender, instance, **kwargs):
    reservation = instance.installment.reservation
    total_amount = reservation.total_amount

    # Calculate the total paid amount for the reservation
    paid_amount = (
        Payment.objects.filter(
            installment__reservation=reservation, installment__installment_status="Paid"
        ).aggregate(total_paid=models.Sum("payment_amount"))["total_paid"]
        or 0
    )

    # Update the reservation payment_status based on the comparison
    if paid_amount >= total_amount:
        reservation.payment_status = "Paid"
    else:
        reservation.payment_status = "Pending"

    reservation.save()


# change availability for room when reservation_status is changed
@receiver(post_save, sender=Reservation)
def update_room_availability(sender, instance, **kwargs):
    not_available_status = [
        Reservation.ReservationStatusChoices.CHECKED_IN,
        Reservation.ReservationStatusChoices.RESERVED,
    ]

    if instance.reservation_status in not_available_status:
        instance.room.is_available = False
    else:
        instance.room.is_available = True

    instance.room.save()


# if reservation is deleted, change room availability
@receiver(post_delete, sender=Reservation)
def update_room_availability_on_delete(sender, instance, **kwargs):
    instance.room.is_available = True
    instance.room.save()


# change is_refunded status if refund is created
@receiver(post_save, sender=Refund)
def update_payment_refunded_status(sender, instance, created, **kwargs):
    if created:
        # Set the is_refunded status of the associated Payment to True
        instance.payment.is_refunded = True
        instance.payment.save()


# Connect the signal
post_save.connect(update_payment_refunded_status, sender=Refund)
