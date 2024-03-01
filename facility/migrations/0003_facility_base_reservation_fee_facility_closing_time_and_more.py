# Generated by Django 5.0.1 on 2024-03-01 15:29

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facility', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='facility',
            name='base_reservation_fee',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Base reservation fee for the facility', max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='facility',
            name='closing_time',
            field=models.TimeField(blank=True, help_text='Closing time of the facility', null=True),
        ),
        migrations.AddField(
            model_name='facility',
            name='extra_person_fee',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Extra person fee for the facility', max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='facility',
            name='max_capacity',
            field=models.PositiveIntegerField(blank=True, help_text='Maximum capacity of the facility', null=True),
        ),
        migrations.AddField(
            model_name='facility',
            name='opening_time',
            field=models.TimeField(blank=True, help_text='Opening time of the facility', null=True),
        ),
        migrations.CreateModel(
            name='FacilityExtraCharge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('Charge', models.DecimalField(decimal_places=2, help_text='Fee for the facility', max_digits=10)),
                ('description', models.CharField(blank=True, help_text='Description of the fee', max_length=255, null=True)),
                ('facility', models.ForeignKey(help_text='Facility associated with the fee', on_delete=django.db.models.deletion.CASCADE, related_name='fees', to='facility.facility')),
            ],
            options={
                'verbose_name': 'Facility Charge',
                'verbose_name_plural': 'Facility Charges',
                'ordering': ['facility', 'Charge'],
            },
        ),
        migrations.CreateModel(
            name='FacilityReservation',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date', models.DateField(help_text='Date of the reservation')),
                ('start_time', models.TimeField(help_text='Time of the reservation')),
                ('end_time', models.TimeField(help_text='End time of the reservation')),
                ('number_of_people', models.PositiveIntegerField(help_text='Number of people for the reservation')),
                ('total_amount', models.DecimalField(blank=True, decimal_places=2, help_text='Total amount for the reservation', max_digits=10, null=True)),
                ('facility', models.ForeignKey(help_text='Facility associated with the reservation', on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='facility.facility')),
                ('user', models.ForeignKey(help_text='User who reserved', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Facility Reservation',
                'verbose_name_plural': 'Facility Reservations',
                'ordering': ['date', 'start_time'],
            },
        ),
    ]