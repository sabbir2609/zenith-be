from django.db.models.signals import post_save
from django.dispatch import receiver
from management.models import Staff, Task
from main.models import Reservation

import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Reservation)
def create_task_on_checked_out(sender, instance, **kwargs):
    """
    Signal handler to create a task when a reservation is checked out.

    Args:
        sender: The sender of the signal (Reservation model).
        instance: The instance of the Reservation model being saved.
        kwargs: Additional keyword arguments.

    Returns:
        None
    """
    if instance.reservation_status == Reservation.ReservationStatusChoices.CHECKED_OUT:
        available_staff = Staff.objects.filter(
            staff_status=Staff.StuffStatusChoices.AVAILABLE
        ).first()

        if available_staff:
            Task.objects.create(assigned_room=instance.room, staff=available_staff)
        else:
            Task.objects.create(assigned_room=instance.room)
            logger.warning("No available staff found for reservation %s", instance)


@receiver(post_save, sender=Task)
def update_staff_on_task_status_change(sender, instance, **kwargs):
    """
    Signal handler to update staff status based on changes in task status.

    Args:
        sender: The sender of the signal (Task model).
        instance: The instance of the Task model being saved.
        kwargs: Additional keyword arguments.

    Returns:
        None
    """
    staff = instance.staff

    if staff:
        if instance.task_status == Task.TaskStatusChoices.PENDING:
            staff.staff_status = Staff.StuffStatusChoices.ASSIGNED
        elif instance.task_status == Task.TaskStatusChoices.IN_PROGRESS:
            staff.staff_status = Staff.StuffStatusChoices.BUSY
        elif instance.task_status == Task.TaskStatusChoices.COMPLETED:
            staff.staff_status = Staff.StuffStatusChoices.AVAILABLE
        else:
            logger.warning("Invalid task status for task %s", instance)
    elif staff is None:
        logger.warning("No staff found for task %s", instance)
        return

    staff.save()


@receiver(post_save, sender=Staff)
def assign_staff_to_pending_tasks(sender, instance, **kwargs):
    """
    Signal handler to assign available staff to pending tasks.

    Args:
        sender: The sender of the signal (Staff model).
        instance: The instance of the Staff model being saved.
        kwargs: Additional keyword arguments.

    Returns:
        None
    """
    if instance.staff_status == Staff.StuffStatusChoices.AVAILABLE:
        # Find tasks with no assigned staff
        pending_tasks = Task.objects.filter(staff=None)

        if pending_tasks.exists():
            # Assign the available staff to the oldest pending task
            oldest_task = pending_tasks.order_by("created_at").first()
            oldest_task.staff = instance
            oldest_task.save()
