# Generated by Django 5.0.7 on 2024-07-27 17:49

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='tags',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, null=True, size=None),
        ),
    ]
