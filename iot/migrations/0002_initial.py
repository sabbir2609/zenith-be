# Generated by Django 4.2.10 on 2024-03-21 06:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('iot', '0001_initial'),
        ('facility', '0001_initial'),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='roomdevice',
            name='room',
            field=models.ForeignKey(help_text='Room in which the device is installed', on_delete=django.db.models.deletion.CASCADE, related_name='devices', to='main.room'),
        ),
        migrations.AddField(
            model_name='facilitydevice',
            name='device',
            field=models.ForeignKey(help_text='Device installed in the facility', on_delete=django.db.models.deletion.CASCADE, to='iot.device'),
        ),
        migrations.AddField(
            model_name='facilitydevice',
            name='facility',
            field=models.ForeignKey(help_text='Facility where the device is installed', on_delete=django.db.models.deletion.CASCADE, related_name='devices', to='facility.facility'),
        ),
        migrations.AddField(
            model_name='device',
            name='device_type',
            field=models.ForeignKey(help_text='Type of the device', on_delete=django.db.models.deletion.CASCADE, to='iot.devicetype'),
        ),
        migrations.AlterUniqueTogether(
            name='roomdevice',
            unique_together={('room', 'device')},
        ),
        migrations.AlterUniqueTogether(
            name='facilitydevice',
            unique_together={('facility', 'device')},
        ),
    ]