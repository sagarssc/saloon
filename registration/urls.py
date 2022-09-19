from django.urls import path

from .views import RegistrationViewSet, SaloonViewSet
from rest_framework import routers


urlpatterns = []

router = routers.DefaultRouter()
router.register('auth', RegistrationViewSet, basename='register')
router.register('saloon', SaloonViewSet, basename='register')

urlpatterns += router.urls