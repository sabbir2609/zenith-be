# Generated by Django 4.2.7 on 2023-12-30 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0013_permission_taskchecklist_rolepermission'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskchecklist',
            name='job',
            field=models.CharField(blank=True, help_text='Job to be performed', max_length=200, null=True),
        ),
    ]
