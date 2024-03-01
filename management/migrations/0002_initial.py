# Generated by Django 5.0.1 on 2024-03-01 14:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0002_initial'),
        ('management', '0001_initial'),
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
            name='for_staff',
            field=models.ForeignKey(blank=True, help_text='Staff for the inventory item', null=True, on_delete=django.db.models.deletion.CASCADE, to='management.staff'),
        ),
        migrations.AddField(
            model_name='task',
            name='assigned_room',
            field=models.ForeignKey(help_text='Assigned room for the task', on_delete=django.db.models.deletion.CASCADE, to='main.room'),
        ),
        migrations.AddField(
            model_name='task',
            name='staff',
            field=models.ForeignKey(blank=True, help_text='Assigned staff for the task', null=True, on_delete=django.db.models.deletion.CASCADE, to='management.staff'),
        ),
        migrations.AddField(
            model_name='taskchecklist',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.task'),
        ),
    ]
