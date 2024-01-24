# Generated by Django 4.2.7 on 2024-01-24 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iot', '0010_rename_device_id_device_client_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='qos',
            field=models.IntegerField(choices=[(0, 'QoS 0'), (1, 'QoS 1'), (2, 'QoS 2'), (3, 'QoS Auto')], default=0, help_text='Quality of Service for the device'),
        ),
    ]
