import random

from rest_framework.authtoken.models import Token
import firebase_admin
import requests
from django.contrib.auth import get_user_model
from firebase_admin import credentials, messaging
from rest_framework import serializers
from tasktracker.models import Location, Machine, Operation, Task, Unit, Plant
from users.models import FcmToken
import datetime
from django.shortcuts import get_object_or_404

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
        r = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={obj.lat}&longitude={obj.lng}&current=temperature_2m&hourly=precipitation_probability&forecast_days=2')
        if r.status_code != 200:
            return r.json()
        time_hours = datetime.datetime.now().hour
        precipitation_probability = r.json().get('hourly').get('precipitation_probability')[time_hours+3]
        temp = r.json().get('current').get('temperature_2m')
        res = {
            'temperature': temp,
            'precipitation_probability_3h_after_now': precipitation_probability,
        }
        return res


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


class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = '__all__'


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
        return instance


class FcmTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = FcmToken
        fields = ('token',)

    def create(self, validated_data, **kwargs):
        user = self.context.get('request').user
        token = validated_data.pop('token')
        instance = FcmToken.objects.create(user=user, token=token)
        return instance
    
    def to_representation(self, instance):
        return {}


def fb_test():
    message = messaging.Message(
        notification=messaging.Notification(
            title='newes title',
            body='newes body'
        ),
        android=messaging.AndroidConfig(
            priority='normal',
            notification=messaging.AndroidNotification(
                icon='stock_ticker_update',
                color='#f45342'
            )
        ),
        apns=messaging.APNSConfig(
            payload=messaging.APNSPayload(
                aps=messaging.Aps(sound='default')
            )
        ),
        token='eynHrwykS-ayyQXFXpsmU0:APA91bHCx3xFfrH5OhTAg_0h77pa3n6UfuQ8LfYcYZzj3YdHyGNt5EU0oDQXk6FIgtR84SE9m0ZJwWkNDzYwtoebJyXJXaZyxZ-jE8-hn6tVm5JI-scanzWObteNZJ47sbBabo5tBpFn',
        data={'bb':'gg'}
    )
    try:
        cred = credentials.Certificate("hackathon-c483e-firebase-adminsdk-lkcji-2a32a0cc39.json")
        firebase_admin.initialize_app(cred)
        messaging.send(message)
    except:
        messaging.send(message)


class RfidSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('rfid',)

    def to_representation(self, instance):
        user = get_object_or_404(User, rfid=instance.get('rfid'))
        token = Token.objects.get_or_create(user=user)[0].key
        return {'Token': token}