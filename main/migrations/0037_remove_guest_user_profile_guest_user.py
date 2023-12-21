# Generated by Django 4.2.7 on 2023-12-21 16:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0036_alter_guest_user_profile_delete_userprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guest',
            name='user_profile',
        ),
        migrations.AddField(
            model_name='guest',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]