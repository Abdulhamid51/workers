# Generated by Django 3.2.9 on 2023-03-04 16:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20230304_1048'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='day',
            options={'ordering': ['-date']},
        ),
        migrations.CreateModel(
            name='BugWork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField(default=0)),
                ('info', models.CharField(max_length=350)),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bugs', to='main.workerprofile')),
            ],
        ),
    ]
