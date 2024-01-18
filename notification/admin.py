from django.contrib import admin

from .models import Notification
from django import forms


class SendNotificationForm(forms.Form):
    message = forms.CharField(label="Notification Message", max_length=255)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ["message", "user", "created_at"]
