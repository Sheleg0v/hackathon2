# Generated by Django 2.2.16 on 2023-11-17 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasktracker', '0002_auto_20231118_0242'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='end_time',
            field=models.DateTimeField(null=True, verbose_name='end_time'),
        ),
        migrations.AddField(
            model_name='task',
            name='start_time',
            field=models.DateTimeField(null=True, verbose_name='start_time'),
        ),
    ]
