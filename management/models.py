import random
import string
import uuid
from django.db import models
from django.conf import settings


class StuffType(models.Model):
    stuff_type = models.CharField(
        max_length=200, help_text="Type or category of the stuff"
    )

    def __str__(self):
        return self.stuff_type

    class Meta:
        verbose_name = "Stuff Type"
        verbose_name_plural = "Stuff Types"


class Stuff(models.Model):
    class StuffStatusChoices(models.TextChoices):
        AVAILABLE = "available", "Available"
        BUSY = "busy", "Busy "

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    staff_id = models.UUIDField(default=uuid.uuid4, help_text="Unique ID of the stuff")
    stuff_type = models.ForeignKey(
        StuffType, on_delete=models.CASCADE, help_text="Type or category of the stuff"
    )
    status = models.CharField(
        max_length=20,
        choices=StuffStatusChoices.choices,
        default=StuffStatusChoices.AVAILABLE,
        help_text="Current status of the stuff",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Date and time of creation"
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="Date and time of the last update"
    )

    def __str__(self):
        return f"{self.user} - {self.stuff_type}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Stuff"
        verbose_name_plural = "Stuffs"


class Task(models.Model):
    class TaskStatusChoices(models.TextChoices):
        PENDING = "pending", "Pending"
        IN_PROGRESS = "in_progress", "In Progress"
        COMPLETED = "completed", "Completed"

    task_id = models.CharField(
        max_length=6,
        unique=True,
        default=None,
        editable=False,
        help_text="6-digit unique identifier for the task",
    )
    task_description = models.CharField(
        max_length=200, default="Prepare The Room", help_text="Description of the task"
    )
    stuff = models.ForeignKey(
        Stuff, on_delete=models.CASCADE, help_text="Assigned stuff for the task"
    )
    task_status = models.CharField(
        max_length=20,
        choices=TaskStatusChoices.choices,
        default=TaskStatusChoices.PENDING,
        help_text="Current status of the task",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Date and time of task creation"
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="Date and time of the last update"
    )

    def save(self, *args, **kwargs):
        # Generate a random 6-digit task_id
        if not self.task_id:
            self.task_id = "".join(random.choices(string.digits, k=6))
        super(Task, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.task_description} - {self.task_status}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
