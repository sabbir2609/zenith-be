# Generated by Django 4.2.7 on 2023-12-19 07:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0027_reservation_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='Guest',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.guest'),
        ),
    ]
