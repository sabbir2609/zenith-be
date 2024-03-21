# Generated by Django 4.2.10 on 2024-03-21 06:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('facility', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='facilityreview',
            name='reviewer',
            field=models.ForeignKey(help_text='User who wrote the review', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='facilityreservation',
            name='facility',
            field=models.ForeignKey(help_text='Facility associated with the reservation', on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='facility.facility'),
        ),
        migrations.AddField(
            model_name='facilityreservation',
            name='user',
            field=models.ForeignKey(help_text='User who reserved', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='facilityimage',
            name='facility',
            field=models.ForeignKey(help_text='Facility associated with the image', on_delete=django.db.models.deletion.CASCADE, related_name='images', to='facility.facility'),
        ),
        migrations.AddField(
            model_name='facilityextracharge',
            name='facility',
            field=models.ForeignKey(help_text='Facility associated with the fee', on_delete=django.db.models.deletion.CASCADE, related_name='extra_charges', to='facility.facility'),
        ),
        migrations.AddField(
            model_name='facilityamenities',
            name='facility',
            field=models.ForeignKey(help_text='Facility associated with the amenities', on_delete=django.db.models.deletion.CASCADE, related_name='amenities', to='facility.facility'),
        ),
    ]
