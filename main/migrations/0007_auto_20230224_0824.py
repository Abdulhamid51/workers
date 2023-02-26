# Generated by Django 3.2.9 on 2023-02-24 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_work_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='workerprofile',
            name='code',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='workerprofile',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='profile_images/'),
        ),
    ]