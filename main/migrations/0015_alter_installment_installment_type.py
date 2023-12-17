# Generated by Django 4.2.7 on 2023-12-17 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_amenity_availability'),
    ]

    operations = [
        migrations.AlterField(
            model_name='installment',
            name='installment_type',
            field=models.CharField(choices=[('First', 'First'), ('Second', 'Second'), ('Third', 'Third')], default='First', max_length=20, unique=True),
        ),
    ]
