# Generated by Django 5.0.1 on 2024-03-01 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facility', '0005_facility_base_capacity_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facility',
            name='description',
            field=models.TextField(blank=True, help_text='Description of the facility', null=True),
        ),
    ]
