# Generated by Django 4.2.7 on 2023-12-17 16:16

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_review_images_alter_reservation_payment_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1, message='Rating must be at least 1.'), django.core.validators.MaxValueValidator(10, message='Rating must be at most 10.')]),
        ),
    ]