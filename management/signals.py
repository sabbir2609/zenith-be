from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from management.models import Task, Stuff
from main.models import Reservation


@receiver(post_save, sender=Reservation)
def create_task_on_checked_out(sender, instance, **kwargs):
    if instance.reservation_status == "checked_out":
        # Check if there is available Stuff
        available_stuff = Stuff.objects.filter(task__isnull=True).first()

        if available_stuff:
            # Create a task and assign the available Stuff
            Task.objects.create(reservation=instance, stuff=available_stuff)
