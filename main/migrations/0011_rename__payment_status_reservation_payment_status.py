# Generated by Django 4.2.7 on 2023-12-16 19:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_rename_payment_status_reservation__payment_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reservation',
            old_name='_payment_status',
            new_name='payment_status',
        ),
    ]
