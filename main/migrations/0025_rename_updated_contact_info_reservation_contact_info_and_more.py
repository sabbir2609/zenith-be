# Generated by Django 4.2.7 on 2023-12-19 06:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_reservation_updated_contact_info_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reservation',
            old_name='updated_contact_info',
            new_name='contact_info',
        ),
        migrations.RenameField(
            model_name='reservation',
            old_name='updated_nid',
            new_name='nid',
        ),
        migrations.AddField(
            model_name='guest',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='guest',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
