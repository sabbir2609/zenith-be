# Generated by Django 5.0.1 on 2024-02-24 15:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_rename_amenity_roomamenity_alter_roomimage_room'),
    ]

    operations = [
        migrations.AlterField(
            model_name='refund',
            name='refund_method',
            field=models.CharField(choices=[('Cash', 'Cash'), ('Card', 'Card'), ('Mobile Banking', 'Mobile Banking')], default='Cash', max_length=20),
        ),
        migrations.AlterField(
            model_name='roomamenity',
            name='room',
            field=models.ForeignKey(help_text='The room to which this amenity is associated.', on_delete=django.db.models.deletion.CASCADE, related_name='amenities', to='main.room'),
        ),
    ]