# Generated by Django 4.2.7 on 2023-12-09 16:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_alter_user_first_name_alter_user_last_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
    ]