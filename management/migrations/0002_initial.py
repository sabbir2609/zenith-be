# Generated by Django 4.2.10 on 2024-03-21 06:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('facility', '0002_initial'),
        ('management', '0001_initial'),
        ('main', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='staff', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='inventory',
            name='for_facility',
            field=models.ForeignKey(blank=True, help_text='Facility for the inventory item', null=True, on_delete=django.db.models.deletion.CASCADE, to='facility.facility'),
        ),
        migrations.AddField(
            model_name='inventory',
            name='for_room',
            field=models.ForeignKey(blank=True, help_text='Room for the inventory item', null=True, on_delete=django.db.models.deletion.CASCADE, to='main.room'),
        ),
        migrations.AddField(
            model_name='inventory',
            name='for_staff',
            field=models.ForeignKey(blank=True, help_text='Staff for the inventory item', null=True, on_delete=django.db.models.deletion.CASCADE, to='management.staff'),
        ),
    ]
