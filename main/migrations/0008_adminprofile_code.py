# Generated by Django 3.2.9 on 2023-02-24 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20230224_0824'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminprofile',
            name='code',
            field=models.IntegerField(default=0),
        ),
    ]
