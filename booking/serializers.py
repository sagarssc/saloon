from django.contrib.auth.models import User
from django.db import models
from django.db.models import fields
from django.contrib.auth.models import Group
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from .models import Booking
from datetime import datetime, time, timedelta, date

class BookingSerializer(serializers.ModelSerializer):

	class Meta:
		model = Booking
		fields = ('id', 'start_time','customer','saloon','service')
	
	def create(self, validated_data):
			booking = Booking(**validated_data)
			booking.end_time = (datetime.combine(date.today(), booking.start_time) + timedelta(minutes=booking.service.time)).time()
			booking.booking_date = datetime.today().date()
			booking.price = booking.service.price
			booking.save()
			return {"status":"success","booking_id":booking.id}
