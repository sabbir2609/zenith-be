# Generated by Django 4.2.7 on 2023-12-19 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0022_review_guest'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guest',
            name='name',
        ),
        migrations.AddField(
            model_name='guest',
            name='nid',
            field=models.CharField(default=4545454545, max_length=100, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='guest',
            name='preferences',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]