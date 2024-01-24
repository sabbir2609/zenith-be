from django.db.models.signals import post_save
from django.dispatch import receiver
from management.models import Staff, Task
from main.models import Reservation

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Reservation)
def create_task_on_checked_out(sender, instance, **kwargs):
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
    if instance.staff_status == Staff.StuffStatusChoices.AVAILABLE:
        pending_tasks = Task.objects.filter(staff=None)

        if pending_tasks.exists():
            oldest_task = pending_tasks.order_by("created_at").first()
            oldest_task.staff = instance
            oldest_task.save()


@receiver(post_save, sender=Task)
def send_notification_on_save(sender, instance, **kwargs):
    from asgiref.sync import async_to_sync
    from channels.layers import get_channel_layer

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "notification_group",
        {
            "type": "on_message",
            "message": f"A new Task Created! - {instance.task_description}",
        },
    )
