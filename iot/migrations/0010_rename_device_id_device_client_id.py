# Generated by Django 4.2.7 on 2024-01-24 18:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('iot', '0009_alter_device_device_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='device',
            old_name='device_id',
            new_name='client_id',
        ),
    ]
