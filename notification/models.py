from django.db import models
from django.conf import settings


class Notification(models.Model):
    message = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message


class Massage(models.Model):
    class Priority(models.TextChoices):
        LOW = "L", "Low"
        MEDIUM = "M", "Medium"
        HIGH = "H", "High"

    message = models.TextField(max_length=100)
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="from_user"
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="to_user"
    )
    priority = models.CharField(
        max_length=1, choices=Priority.choices, default=Priority.LOW
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message
