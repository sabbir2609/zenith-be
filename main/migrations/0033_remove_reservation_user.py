# Generated by Django 4.2.7 on 2023-12-21 16:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0032_rename_contact_info_guest_contact_number_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='user',
        ),
    ]