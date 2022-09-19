from django.urls import path

from .views import BookingViewSet
from rest_framework import routers


urlpatterns = []

router = routers.DefaultRouter()
router.register('', BookingViewSet, basename='register')

urlpatterns += router.urls