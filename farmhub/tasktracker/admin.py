from django.contrib import admin
from .models import *


class MachineAdmin(admin.ModelAdmin):
    list_display = ('name', 'registration_number')


class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'serial_number')


class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'lat', 'lng')


class OperationAdmin(admin.ModelAdmin):
    list_display = ('type', 'speed', 'depth', 'flowrate')


class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'add_date',
        'commit_date',
        'start_time',
        'end_time',
        'operation',
        'status',
        'payment',
        'machine',
        'unit',
        'location',
        'executor',
        'comment'
    )


admin.site.register(Machine, MachineAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Operation, OperationAdmin)
admin.site.register(Task, TaskAdmin)