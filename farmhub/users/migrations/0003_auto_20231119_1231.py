# Generated by Django 2.2.16 on 2023-11-19 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_fcmtoken'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fcmtoken',
            name='token',
            field=models.CharField(max_length=250, unique=True, verbose_name='fcm_token'),
        ),
    ]
