# Generated by Django 5.0.1 on 2024-03-01 14:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('facility', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the device type', max_length=100)),
                ('description', models.TextField(blank=True, help_text='Description of the device type', null=True)),
            ],
            options={
                'verbose_name': 'Device Type',
                'verbose_name_plural': 'Device Types',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(help_text='Name of the device', max_length=100)),
                ('client_id', models.CharField(help_text='Unique identifier for the device', max_length=100, unique=True)),
                ('topic', models.CharField(blank=True, help_text='MQTT topic for the device', max_length=100, null=True)),
                ('qos', models.IntegerField(choices=[(0, 'QoS 0'), (1, 'QoS 1'), (2, 'QoS 2'), (3, 'QoS Auto')], default=0, help_text='Quality of Service for the device')),
                ('status', models.BooleanField(default=False, help_text='Status of the device (active/inactive)')),
                ('description', models.TextField(blank=True, help_text='Description of the device', null=True)),
                ('installation_date', models.DateField(help_text='Date when the device was installed')),
                ('device_type', models.ForeignKey(help_text='Type of the device', on_delete=django.db.models.deletion.CASCADE, to='iot.devicetype')),
            ],
            options={
                'verbose_name': 'Device',
                'verbose_name_plural': 'Devices',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='FacilityDevice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device', models.ForeignKey(help_text='Device installed in the facility', on_delete=django.db.models.deletion.CASCADE, to='iot.device')),
                ('facility', models.ForeignKey(help_text='Facility where the device is installed', on_delete=django.db.models.deletion.CASCADE, related_name='devices', to='facility.facility')),
            ],
            options={
                'verbose_name': 'Facility Device',
                'verbose_name_plural': 'Facility Devices',
            },
        ),
        migrations.CreateModel(
            name='RoomDevice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device', models.ForeignKey(help_text='Device installed in the room', on_delete=django.db.models.deletion.CASCADE, to='iot.device')),
            ],
            options={
                'verbose_name': 'Room Device',
                'verbose_name_plural': 'Room Devices',
            },
        ),
    ]
