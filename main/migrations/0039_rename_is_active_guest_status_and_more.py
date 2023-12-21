# Generated by Django 4.2.7 on 2023-12-21 18:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0038_alter_guest_contact_info_alter_guest_nid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='guest',
            old_name='is_active',
            new_name='status',
        ),
        migrations.RemoveField(
            model_name='installment',
            name='installment_id',
        ),
        migrations.AddField(
            model_name='reservation',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='reservation',
            name='guest',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='main.guest'),
        ),
    ]