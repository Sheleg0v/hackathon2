# Generated by Django 2.2.16 on 2023-11-18 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasktracker', '0004_remove_operation_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='comment',
            field=models.TextField(blank=True, null=True, verbose_name='comment'),
        ),
        migrations.AlterField(
            model_name='task',
            name='end_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='end_time'),
        ),
        migrations.AlterField(
            model_name='task',
            name='payment',
            field=models.FloatField(blank=True, null=True, verbose_name='payment'),
        ),
        migrations.AlterField(
            model_name='task',
            name='start_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='start_time'),
        ),
    ]
