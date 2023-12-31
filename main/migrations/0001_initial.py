# Generated by Django 4.2.7 on 2023-12-16 10:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Guest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('contact_info', models.CharField(max_length=100)),
                ('preferences', models.CharField(max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Guest',
            },
        ),
        migrations.CreateModel(
            name='RoomType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_type', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'Room Type',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_id', models.CharField(max_length=100)),
                ('capacity', models.IntegerField()),
                ('images', models.ImageField(blank=True, null=True, upload_to='room/')),
                ('description', models.TextField()),
                ('availability', models.BooleanField(default=True)),
                ('room_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.roomtype')),
            ],
            options={
                'verbose_name_plural': 'Room',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('comment', models.TextField()),
                ('guest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.guest')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.room')),
            ],
            options={
                'verbose_name_plural': 'Reviews',
            },
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reservation_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('status', models.CharField(max_length=100)),
                ('guest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.guest')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.room')),
            ],
            options={
                'verbose_name_plural': 'Reservation',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('reservation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.reservation')),
            ],
            options={
                'verbose_name_plural': 'Payment',
            },
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('status', models.CharField(max_length=100)),
                ('reservation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.reservation')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.room')),
            ],
            options={
                'verbose_name_plural': 'Booking',
            },
        ),
        migrations.CreateModel(
            name='Amenity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.room')),
            ],
            options={
                'verbose_name_plural': 'Amenity',
            },
        ),
    ]
