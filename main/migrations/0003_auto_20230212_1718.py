# Generated by Django 3.2.9 on 2023-02-12 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_work_sum'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminprofile',
            name='gave_money',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='adminprofile',
            name='workers_money',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
