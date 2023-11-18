from django.contrib.auth.models import AbstractUser
from django.db import models

ROLES = (
    ('AGRICULTURIST', 'agriculturist'),
    ('MECHANIZER', 'mechanizer'),
    ('DISPATCHER', 'dispatcher'),
)


class User(AbstractUser):
    rfid = models.CharField(verbose_name='rfid', max_length=255)
    first_name = models.CharField(verbose_name='first_name', max_length=255)
    last_name = models.CharField(verbose_name='last_name', max_length=255)
    middle_name = models.CharField(verbose_name='middle_name', max_length=255)
    employee_id = models.CharField(verbose_name='employee_id', max_length=255)
    role = models.CharField(
        'role',
        choices=ROLES,
        default='OPEN',
        max_length=255
    )
    phone = models.CharField(verbose_name='phone', max_length=255)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
