from notification.models import Massage
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from notification.models import Notification
from django.utils import timezone
from notification.channels.consumers import NotificationConsumer


def notify_user(sender, instance, created, **kwargs):
    pass
