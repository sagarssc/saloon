from django.http import JsonResponse
from .models import Saloon
from booking.models import Booking
from rest_framework.decorators import action, permission_classes
from rest_framework import permissions, serializers
from rest_framework.authtoken.models import Token
from rest_framework import viewsets
from .serializers import RegisterSerializer
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User, Group
from dateutil.relativedelta import relativedelta
from datetime import datetime
from django.db.models import Sum, Count

class RegistrationViewSet(viewsets.ModelViewSet):
	serializer_class = RegisterSerializer
	# http_method_names = ['post']

	@action(detail=False, methods=["post"],permission_classes=[])
	def register(self, request, pk=None, *args, **kwargs):
		data = request.data
		serializer = self.get_serializer(data=data)
		serializer.is_valid(raise_exception=True)
		user = serializer.save()
		token = Token.objects.get_or_create(user=user)
		return JsonResponse({"id":user.id,"username":user.username, "token": str(token[0])})

	@action(detail=False,methods=['post'],permission_classes=[])
	def login(self, request, *args, **kwargs):
		data = request.data
		user = authenticate(username = data.get("username"),password = data.get("password"))
		if user and user.is_active:
			is_tokened = Token.objects.filter(user=user).exists()
			if is_tokened:
			  user.auth_token.delete()
			token = Token.objects.get_or_create(user=user)
			return JsonResponse({
				"id":user.id,"username":user.username, "token": str(token[0])
			})
		else:
			raise serializers.ValidationError('Incorrect Credentials Passed.')


class SaloonViewSet(viewsets.ModelViewSet):

	@action(detail=False, methods=["post"],permission_classes=[IsAuthenticated])
	def register(self, request, pk=None, *args, **kwargs):
		data = request.data
		token = request.headers.get('Authorization').split()[1]
		user = Token.objects.get(key=token).user
		group = Group.objects.filter(name="SaloonOwner").last()
		group.user_set.add(user)
		saloon = Saloon()
		data["owner"] = user
		saloon = saloon.add_saloon(data)
		return JsonResponse({"id":user.id,"username":user.username, "saloon_name":saloon.name})

	@action(detail=True, methods=["post"],permission_classes=[IsAuthenticated])
	def add_service(self, request, pk=None, *args, **kwargs):
		data = request.data
		token = request.headers.get('Authorization').split()[1]
		user = Token.objects.get(key=token).user
		saloon = Saloon.objects.get(id=pk)
		if user.id == saloon.owner_id:
			for service in data['services']:
				saloon.add_service(service)
			return JsonResponse({"status":"success"})
		else:
			return JsonResponse({"status":"failed","msg":"you dont have access for this saloon"})

	@action(detail=True, methods=["post"],permission_classes=[IsAuthenticated])
	def add_schdule(self, request, pk=None, *args, **kwargs):
		data = request.data
		token = request.headers.get('Authorization').split()[1]
		user = Token.objects.get(key=token).user
		saloon = Saloon.objects.get(id=pk)
		if user.id == saloon.owner_id:
			for schdule in data['schdules']:
				saloon.add_schdule(schdule)
			return JsonResponse({"status":"success"})
		else:
			return JsonResponse({"status":"failed","msg":"you dont have access for this saloon"})

	@action(detail=True, methods=["get"],permission_classes=[IsAuthenticated])
	def get_revenue_details(self, request, pk=None, *args, **kwargs):
		token = request.headers.get('Authorization').split()[1]
		user = Token.objects.get(key=token).user
		saloon = Saloon.objects.get(id=pk)
		if user.id == saloon.owner_id:
			data = {}
			start_date = datetime.today() - relativedelta(months=1)
			end_date = datetime.today()
			bookings = Booking.objects.filter(saloon_id=saloon.id,booking_date__gte=start_date,booking_date__lte=end_date)
			cancelled_bookings = bookings.filter(is_cancelled=True)
			completed_bookings = bookings.filter(is_cancelled=False)
			booking_data = list(completed_bookings.values('service__name').annotate(price=Sum('price'), count=Count('id')))
			data["revenue"] = sum(service['price'] for service in booking_data)
			data["total_services"] = sum(service['count'] for service in booking_data)
			data["services"] = booking_data
			data["revenue_loss"] = 0
			for cb in cancelled_bookings:
				bookings_at_cancelled_slot = Booking.objects.filter(booking_date=cb.booking_date,start_time__lte=cb.start_time,end_time__gte=cb.end_time,is_cancelled=False).count()
				if saloon.no_of_sheets > bookings_at_cancelled_slot:
					data["revenue_loss"] += cb.price
			return JsonResponse(data)
		else:
			return JsonResponse({"status":"failed","msg":"you dont have access for this saloon"})