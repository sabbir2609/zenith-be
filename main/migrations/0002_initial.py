# Generated by Django 4.2.10 on 2024-03-21 06:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='refund',
            name='payment',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='refund', to='main.payment'),
        ),
        migrations.AddField(
            model_name='payment',
            name='installment',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='payment', to='main.installment'),
        ),
        migrations.AddField(
            model_name='installment',
            name='reservation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='installments', to='main.reservation'),
        ),
        migrations.AddField(
            model_name='guest',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='room',
            unique_together={('floor', 'room_label')},
        ),
    ]
