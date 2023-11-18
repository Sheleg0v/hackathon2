import random

import firebase_admin
import requests
from django.contrib.auth import get_user_model
from firebase_admin import credentials
from rest_framework import serializers
from tasktracker.models import Location, Machine, Operation, Task, Unit

User = get_user_model()


class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = '__all__'


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    weather = serializers.SerializerMethodField()

    class Meta:
        model = Location
        fields = '__all__'

    def get_weather(self, obj):

        r = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={obj.lat}&longitude={obj.lng}&current=temperature_2m,rain,wind_speed_10m')
        return r.json()


class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'rfid',
            'first_name',
            'last_name',
            'middle_name',
            'employee_id',
            'role',
            'phone',
        )


class TaskReadSerializer(serializers.ModelSerializer):
    machine = MachineSerializer()
    unit = UnitSerializer()
    location = LocationSerializer()
    operation = OperationSerializer()
    executor = UserSerializer()
    author = UserSerializer()

    class Meta:
        model = Task
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    operation = OperationSerializer()

    class Meta:
        model = Task
        fields = '__all__'

    def to_representation(self, instance):
        serializer = TaskReadSerializer(instance)
        return serializer.data

    def create(self, validated_data, **kwargs):
        operation = validated_data.pop('operation')
        instance = Task(**validated_data)
        operation_serializer = OperationSerializer(data=operation)
        if operation_serializer.is_valid():
            instance.operation = operation_serializer.save()

        if instance.status == 'CLOSED':
            instance.payment = random.randrange(5000, 10000)

        instance.save()
        return instance

    def update(self, instance, validated_data):
        operation = validated_data.pop('operation')
        operation_serializer = OperationSerializer(data=operation)
        instance = super().update(instance, validated_data)
        if operation_serializer.is_valid():
            instance.operation = operation_serializer.save()
        instance.save()


        # fb_test()


        return instance


def fb_test():
    cred = credentials.Certificate("../../hackathon-c483e-firebase-adminsdk-lkcji-2a32a0cc39.json")
    firebase_admin.initialize_app(cred)

    message = firebase_admin.messaging
