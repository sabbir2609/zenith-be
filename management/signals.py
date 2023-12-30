import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from management.models import Task, Staff
from main.models import Reservation

# Get an instance of a logger
logger = logging.getLogger(__name__)


@receiver(post_save, sender=Reservation)
def create_task_on_checked_out(sender, instance, **kwargs):
    if instance.reservation_status == Reservation.ReservationStatusChoices.CHECKED_OUT:
        # Check if there is available staff
        available_staff = Staff.objects.filter(
            staff_status=Staff.StuffStatusChoices.AVAILABLE
        ).first()

        if available_staff:
            Task.objects.create(assigned_room=instance.room, staff=available_staff)
        else:
            logger.warning("No available staff found for reservation %s", instance)


@receiver(post_save, sender=Task)
def update_staff_on_task_status_change(sender, instance, **kwargs):
    staff = instance.staff

    if instance.task_status == Task.TaskStatusChoices.PENDING:
        staff.staff_status = Staff.StuffStatusChoices.ASSIGNED
    elif instance.task_status == Task.TaskStatusChoices.IN_PROGRESS:
        staff.staff_status = Staff.StuffStatusChoices.BUSY
    elif instance.task_status == Task.TaskStatusChoices.COMPLETED:
        staff.staff_status = Staff.StuffStatusChoices.AVAILABLE
    else:
        print("Invalid task status")

    staff.save()
