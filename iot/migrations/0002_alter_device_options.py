# Generated by Django 4.2.7 on 2024-01-20 19:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('iot', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='device',
            options={'ordering': ['-created_at'], 'verbose_name': 'Device', 'verbose_name_plural': 'Devices'},
        ),
    ]
