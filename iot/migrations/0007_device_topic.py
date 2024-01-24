# Generated by Django 4.2.7 on 2024-01-24 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iot', '0006_remove_device_facility_remove_device_room_roomdevice_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='topic',
            field=models.CharField(blank=True, help_text='MQTT topic for the device', max_length=100, null=True),
        ),
    ]
