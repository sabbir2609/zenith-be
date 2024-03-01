# Generated by Django 5.0.1 on 2024-03-01 14:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='guest',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='payment',
            name='installment',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='payment', to='main.installment'),
        ),
        migrations.AddField(
            model_name='refund',
            name='payment',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='refund', to='main.payment'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='guest',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='main.guest'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='installment',
            name='reservation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='installments', to='main.reservation'),
        ),
        migrations.AddField(
            model_name='review',
            name='guest',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='main.guest'),
        ),
        migrations.AddField(
            model_name='review',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='review_likes', to='main.guest'),
        ),
        migrations.AddField(
            model_name='room',
            name='floor',
            field=models.ForeignKey(help_text='The floor to which this room belongs.', on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to='main.floor'),
        ),
        migrations.AddField(
            model_name='review',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='main.room'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='main.room'),
        ),
        migrations.AddField(
            model_name='roomamenity',
            name='room',
            field=models.ForeignKey(help_text='The room to which this amenity is associated.', on_delete=django.db.models.deletion.CASCADE, related_name='amenities', to='main.room'),
        ),
        migrations.AddField(
            model_name='roomimage',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='main.room'),
        ),
        migrations.AddField(
            model_name='room',
            name='room_type',
            field=models.ForeignKey(help_text='The type or category of the room.', on_delete=django.db.models.deletion.CASCADE, to='main.roomtype'),
        ),
        migrations.AlterUniqueTogether(
            name='room',
            unique_together={('floor', 'room_label')},
        ),
    ]
