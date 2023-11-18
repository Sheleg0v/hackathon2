
from django_filters import rest_framework as filters
from rest_framework import mixins, permissions, viewsets
from tasktracker.models import *
from users.models import FcmToken

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