# Generated by Django 4.2.7 on 2023-12-30 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stuff',
            name='is_available',
            field=models.BooleanField(default=True, help_text='Status of the stuff'),
        ),
    ]