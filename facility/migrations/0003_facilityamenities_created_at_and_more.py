# Generated by Django 5.0.1 on 2024-02-27 18:30

import datetime
import django.db.models.deletion
import facility.models
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facility', '0002_facility_is_reservable_facilityreservation_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='facilityamenities',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2024, 2, 27, 18, 29, 36, 417320, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='facilityamenities',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='facilityimage',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2024, 2, 27, 18, 29, 49, 193231, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='facilityimage',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='facilityreservation',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2024, 2, 27, 18, 29, 56, 473245, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='facilityreservation',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='facilityreview',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2024, 2, 27, 18, 30, 2, 9339, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='facilityreview',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='facilityreview',
            name='rating',
            field=models.DecimalField(decimal_places=1, help_text='Rating of the facility', max_digits=2),
        ),
        migrations.CreateModel(
            name='Installment',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.CharField(default=facility.models.generate_unique_id, editable=False, max_length=50, primary_key=True, serialize=False, unique=True)),
                ('installment_type', models.CharField(choices=[('First', 'First'), ('Second', 'Second'), ('Third', 'Third'), ('Full', 'Full')], default='First', max_length=20)),
                ('installment_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('installment_status', models.CharField(default='Pending', max_length=20)),
                ('reservation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='installments', to='facility.facilityreservation')),
            ],
            options={
                'verbose_name': 'Installment',
                'verbose_name_plural': 'Installments',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('payment_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_method', models.CharField(choices=[('Cash', 'Cash'), ('Card', 'Card'), ('Mobile Banking', 'Mobile Banking')], default='Cash', max_length=20)),
                ('is_refunded', models.BooleanField(default=False)),
                ('installment', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='payment', to='facility.installment')),
            ],
            options={
                'verbose_name': 'Payment',
                'verbose_name_plural': 'Payments',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Refund',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('refund_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('refund_method', models.CharField(choices=[('Cash', 'Cash'), ('Card', 'Card'), ('Mobile Banking', 'Mobile Banking')], default='Cash', max_length=20)),
                ('payment', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='refund', to='facility.payment')),
            ],
            options={
                'verbose_name': 'Refund',
                'verbose_name_plural': 'Refunds',
                'ordering': ['-created_at'],
            },
        ),
        migrations.DeleteModel(
            name='FacilityInstallment',
        ),
    ]