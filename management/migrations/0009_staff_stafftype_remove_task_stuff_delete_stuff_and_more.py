# Generated by Django 4.2.7 on 2023-12-30 18:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('management', '0008_alter_task_stuff'),
    ]

    operations = [
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('staff_id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID of the staff')),
                ('staff_status', models.CharField(choices=[('available', 'Available'), ('busy', 'Busy '), ('assigned', 'Assigned')], default='available', help_text='Current status of the staff', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date and time of creation')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Date and time of the last update')),
            ],
            options={
                'verbose_name': 'staff',
                'verbose_name_plural': 'Stuffs',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='StaffType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('staff_type', models.CharField(help_text='Type or category of the staff', max_length=200)),
            ],
            options={
                'verbose_name': 'staff Type',
                'verbose_name_plural': 'staff Types',
            },
        ),
        migrations.RemoveField(
            model_name='task',
            name='stuff',
        ),
        migrations.DeleteModel(
            name='Stuff',
        ),
        migrations.DeleteModel(
            name='StuffType',
        ),
        migrations.AddField(
            model_name='staff',
            name='staff_type',
            field=models.ForeignKey(help_text='Type or category of the staff', on_delete=django.db.models.deletion.CASCADE, to='management.stafftype'),
        ),
        migrations.AddField(
            model_name='staff',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='task',
            name='staff',
            field=models.ForeignKey(blank=True, help_text='Assigned staff for the task', null=True, on_delete=django.db.models.deletion.CASCADE, to='management.staff'),
        ),
    ]
