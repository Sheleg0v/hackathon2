from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter


from users.views import sign_up

from .views import *

app_name = 'api'

router = DefaultRouter()
router.register('machine', MachineViewSet, basename='machine')
router.register('unit', UnitViewSet, basename='unit')
router.register('location', LocationViewSet, basename='location')
router.register('task', TaskViewSet, basename='task')
router.register('user', UserViewSet, basename='user')
router.register('fcm_token', FcmTokenViewSet, basename='fcm_token')
router.register('plant', PlantViewSet, basename='plant')
router.register('rfid_auth', RfidViewSet, basename='rfid_auth')


urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token),
    path(
        'sign_up/',
        sign_up,
        name='sign_up'
    ),
    path('', include(router.urls)),
]
