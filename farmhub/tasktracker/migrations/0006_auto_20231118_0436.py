# Generated by Django 2.2.16 on 2023-11-18 01:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasktracker', '0005_auto_20231118_0434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='add_date',
            field=models.DateField(verbose_name='AddDate'),
        ),
        migrations.AlterField(
            model_name='task',
            name='commit_date',
            field=models.DateField(verbose_name='CommitDate'),
        ),
    ]
