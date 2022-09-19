from django.http import JsonResponse
from registration.models import Saloon, Service
from rest_framework.decorators import action, permission_classes
from rest_framework import permissions, serializers
from rest_framework.authtoken.models import Token
from rest_framework import viewsets
from .serializers import BookingSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User, Group
from datetime import datetime
from .utils import get_all_slots
from .models import Booking

class BookingViewSet(viewsets.ModelViewSet):
	serializer_class = BookingSerializer


	@action(detail=False, methods=["get"],permission_classes=[IsAuthenticated])
	def get_slots(self, request, pk=None, *args, **kwargs):
		data = request.GET
		service_id = data['service_id']
		data = get_all_slots(service_id)
		return JsonResponse(data, safe=False)

	@action(detail=False, methods=["post"],permission_classes=[IsAuthenticated])
	def book_service(self, request, pk=None, *args, **kwargs):
		data = request.data
		token = request.headers.get('Authorization').split()[1]
		user = Token.objects.get(key=token).user
		booking_data = {}
		booking_data["saloon"] = data['saloon_id']
		booking_data["service"] = data['service_id']
		booking_data["start_time"] = data["booking_time"]
		booking_data["customer"] = user.id
		serializer = self.get_serializer(data=booking_data)
		serializer.is_valid(raise_exception=True)
		data = serializer.save()
		return JsonResponse(data)

	@action(detail=True, methods=["post"],permission_classes=[IsAuthenticated])
	def cancel_service(self, request, pk=None, *args, **kwargs):
		data = request.data
		token = request.headers.get('Authorization').split()[1]
		user = Token.objects.get(key=token).user
		booking = Booking.objects.get(id=pk)
		if booking.customer == user:
			booking.is_cancelled = True
			booking.save()
			return JsonResponse({"status":"success"})
		else:
			return JsonResponse({"status":"failed","msg":"you cant cancel this service"})


	

