# Generated by Django 4.2.7 on 2023-12-16 13:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_reservation_options_alter_amenity_description_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Installment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('due_date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='reservation',
            options={},
        ),
        migrations.RenameField(
            model_name='reservation',
            old_name='status',
            new_name='reservation_status',
        ),
        migrations.AddField(
            model_name='reservation',
            name='payment_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Partial', 'Partial'), ('Paid', 'Paid')], default='Paid', max_length=20),
        ),
        migrations.DeleteModel(
            name='Payment',
        ),
        migrations.AddField(
            model_name='installment',
            name='reservation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.reservation'),
        ),
    ]
