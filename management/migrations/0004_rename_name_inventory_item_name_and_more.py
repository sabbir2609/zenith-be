# Generated by Django 5.0.1 on 2024-02-14 18:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0003_inventory'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inventory',
            old_name='name',
            new_name='item_name',
        ),
        migrations.RenameField(
            model_name='inventory',
            old_name='quantity',
            new_name='item_quantity',
        ),
    ]