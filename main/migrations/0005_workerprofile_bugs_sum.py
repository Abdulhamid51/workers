# Generated by Django 3.2.9 on 2023-03-04 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_bugwork_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='workerprofile',
            name='bugs_sum',
            field=models.IntegerField(default=0),
        ),
    ]
