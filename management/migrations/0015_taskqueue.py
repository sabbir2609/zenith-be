# Generated by Django 4.2.7 on 2023-12-30 19:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0014_taskchecklist_job'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskQueue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('task', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='management.task')),
            ],
        ),
    ]
