# Generated by Django 4.2.7 on 2023-12-31 09:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0016_alter_taskqueue_task'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rolepermission',
            name='permission',
        ),
        migrations.RemoveField(
            model_name='rolepermission',
            name='role',
        ),
        migrations.RemoveField(
            model_name='taskqueue',
            name='task',
        ),
        migrations.DeleteModel(
            name='Permission',
        ),
        migrations.DeleteModel(
            name='RolePermission',
        ),
        migrations.DeleteModel(
            name='TaskQueue',
        ),
    ]
