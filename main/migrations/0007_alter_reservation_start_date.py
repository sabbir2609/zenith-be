# Generated by Django 4.2.7 on 2023-12-16 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_reservation_payment_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
