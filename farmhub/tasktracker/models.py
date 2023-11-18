from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Machine(models.Model):
    name = models.CharField(verbose_name='name', max_length=255)
    registration_number = models.CharField(verbose_name='registration_number', max_length=255)


class Unit(models.Model):
    name = models.CharField(verbose_name='name', max_length=255)
    serial_number = models.CharField(verbose_name='serial_number', max_length=255)


class Location(models.Model):
    name = models.CharField(verbose_name='name', max_length=255)
    lat = models.FloatField(verbose_name='lat')
    lng = models.FloatField(verbose_name='lng')


TYPES = (
    ('SEEDING', 'seeding'),
    ('PROTECTION', 'protection'),
    ('HARVESTING', 'harvesting'),
    ('SOIL_PREPARATION', 'soil_preparation'),
)


class Operation(models.Model):
    type = models.CharField(
        'type',
        choices=TYPES,
        max_length=255
    )
    speed = models.FloatField(verbose_name='speed')
    depth = models.FloatField(verbose_name='depth')
    flowrate = models.FloatField(verbose_name='flowrate')


STATUSES = (
    ('OPEN', 'open'),
    ('MACHINE_INSPECTION', 'machine_inspection'),
    ('IN_PROGRESS', 'in_progres'),
    ('CLOSED', 'closed'),
    ('PAUSED', 'paused'),
    ('DONE', 'done'),
)


class Plant(models.Model):
    name = models.CharField(
        verbose_name='plant_name',
        max_length=250
    )


class Task(models.Model):
    add_date = models.DateTimeField(verbose_name='AddDate')
    commit_date = models.DateTimeField(verbose_name='CommitDate')
    start_time = models.DateTimeField(verbose_name='start_time', null=True,  blank=True)
    end_time = models.DateTimeField(verbose_name='end_time', null=True, blank=True)
    operation = models.ForeignKey(
        Operation,
        on_delete=models.CASCADE,
        verbose_name='operation',
        related_name='task'
    )
    status = models.CharField(
        'status',
        choices=STATUSES,
        default='OPEN',
        max_length=255
    )
    payment = models.FloatField(
        verbose_name='payment',
        null=True,
        blank=True
    )
    machine = models.ForeignKey(
        Machine,
        on_delete=models.CASCADE,
        verbose_name='machine',
        related_name='task'
    )
    unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
        verbose_name='unit',
        related_name='task'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        verbose_name='location',
        related_name='task'
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='executor',
        related_name='executor_task'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='author',
        related_name='author_task'
    )
    comment = models.TextField(
        verbose_name='comment',
        null=True,
        blank=True
    )
    plant = models.ForeignKey(
        Plant,
        verbose_name='plant',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
