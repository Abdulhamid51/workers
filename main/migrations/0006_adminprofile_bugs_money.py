# Generated by Django 3.2.9 on 2023-03-04 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_workerprofile_bugs_sum'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminprofile',
            name='bugs_money',
            field=models.IntegerField(default=0),
        ),
    ]