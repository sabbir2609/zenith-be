import random
import string
import uuid
from django.db import models
from django.conf import settings

from main.models import Room
from facility.models import Facility


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Role(models.Model):
    name = models.CharField(max_length=200, help_text="Type or category of the staff")
    description = models.TextField(
        null=True, blank=True, help_text="Description of the role"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Role"
        verbose_name_plural = "Role"
        ordering = ["id"]


class Staff(BaseModel):
    class StuffStatusChoices(models.TextChoices):
        AVAILABLE = "available", "Available"
        BUSY = "busy", "Busy "
        ASSIGNED = "assigned", "Assigned"

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    staff_id = models.UUIDField(default=uuid.uuid4, help_text="Unique ID of the staff")
    role = models.ForeignKey(
        Role, on_delete=models.CASCADE, help_text="Role of the staff"
    )
    staff_status = models.CharField(
        max_length=20,
        choices=StuffStatusChoices.choices,
        default=StuffStatusChoices.AVAILABLE,
        help_text="Current status of the staff",
    )

    def __str__(self):
        return f"{self.user} - {self.role}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "staff"
        verbose_name_plural = "Staffs"


class Task(BaseModel):
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
    assigned_room = models.ForeignKey(
        Room, on_delete=models.CASCADE, help_text="Assigned room for the task"
    )
    staff = models.ForeignKey(
        Staff,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Assigned staff for the task",
    )
    task_status = models.CharField(
        max_length=20,
        choices=TaskStatusChoices.choices,
        default=TaskStatusChoices.PENDING,
        help_text="Current status of the task",
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


class TaskCheckList(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    job = models.CharField(
        max_length=200, null=True, blank=True, help_text="Job to be performed"
    )
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.task} - {self.check_list}"

    class Meta:
        verbose_name = "Task Check List"
        verbose_name_plural = "Task Check Lists"


class Inventory(BaseModel):
    item_name = models.CharField(max_length=200, help_text="Name of the inventory item")
    item_quantity = models.IntegerField(help_text="Quantity of the inventory item")
    for_room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Room for the inventory item",
    )
    for_facility = models.ForeignKey(
        Facility,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Facility for the inventory item",
    )
    for_staff = models.ForeignKey(
        Staff,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Staff for the inventory item",
    )

    def __str__(self):
        return f"{self.item_name} - {self.item_quantity}"

    class Meta:
        verbose_name = "Inventory Item"
        verbose_name_plural = "Inventory Items"
        ordering = ["-created_at"]
