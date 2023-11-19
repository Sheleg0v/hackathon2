
from django_filters import rest_framework as filters
from rest_framework import mixins, permissions, viewsets
from tasktracker.models import *
from users.models import FcmToken
from django.shortcuts import get_object_or_404
import firebase_admin
from firebase_admin import credentials, messaging
from django.shortcuts import HttpResponse

from .serializers import (
    TaskSerializer,
    UserSerializer,
    LocationSerializer,
    UnitSerializer,
    MachineSerializer,
    FcmTokenSerializer,
    PlantSerializer,
    RfidSerializer
)


class MachineViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer
    permission_classes = (permissions.IsAuthenticated,)


class UnitViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    permission_classes = (permissions.IsAuthenticated,)


class LocationViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = (permissions.IsAuthenticated,)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('machine', 'unit', 'operation', 'executor', 'author', 'status')

    def update(self, request, *args, **kwargs):
        user = request.user
        id = kwargs.get('pk')
        task = get_object_or_404(Task, id=id)
        if task.author == user:
            self.send_push(task.executor, title='Изменения задание', body='В ваше задание были внесены изменения')
        elif task.executor == user and (task.status == 'DONE' or task.status == 'PAUSED'):
            self.send_push(task.author, title='Изменения статуса задания', body='В вашего задания изменился статус')

        return super().update(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        executor_id = request.data.get('executor')
        executor = get_object_or_404(User, id=executor_id)
        self.send_push(executor, 'У вас новое задание', 'Вам выдали новое задание')

        return super().create(request, *args, **kwargs)

    def send_push(self, user, title, body):
        tokens = FcmToken.objects.filter(user=user)
        for token in tokens:
            try:
                message = messaging.Message(
                    notification=messaging.Notification(
                        title=title,
                        body=body
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
                    token=token.token,
                    data={'bb':'gg'}
                )
            except:
                continue
            try:
                cred = credentials.Certificate("hackathon-c483e-firebase-adminsdk-lkcji-2a32a0cc39.json")
                firebase_admin.initialize_app(cred)
                messaging.send(message)
            except:
                try:
                    messaging.send(message)
                except:
                    pass


class UserViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)


class FcmTokenViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = FcmToken.objects.all()
    serializer_class = FcmTokenSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        token = request.data.get('token')
        tokens = FcmToken.objects.filter(token=token)
        if len(tokens) != 0:
            return HttpResponse()
        return super().create(request, *args, **kwargs)


class PlantViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer
    permission_classes = (permissions.IsAuthenticated,)


class RfidViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = User.objects.all()
    serializer_class = RfidSerializer

    def perform_create(self, serializer):
        return 