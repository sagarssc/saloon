from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date, time, timedelta
import jsonfield
import math
# Create your models here
class Saloon(models.Model):
	name = models.CharField(max_length=50, null=False, unique=True)
	gstin = models.CharField(max_length=15, null=False)
	pan_no = models.CharField(max_length=10, null=False, unique=True)
	address = models.CharField(max_length=300, null=False)
	no_of_sheets = models.IntegerField(default=0)
	owner = models.ForeignKey(User, related_name = 'saloons', on_delete=models.CASCADE)

	def add_saloon(self, data):
		saloon = Saloon.objects.create(
			name = data['name'],
			gstin = data['gst_in'],
			pan_no = data['pan_no'],
			address = data['address'],
			no_of_sheets = data['no_of_sheets'],
			owner = data['owner']
		)
		return saloon
	
	def add_service(self, data):
		self.services.create(**data)
	
	def add_schdule(self, data):
		self.schdules.create(**data)
	
	def get_schdule(self):
		booking_date = 	datetime.today()
		day = booking_date.strftime('%A').lower()
		schdule = self.schdules.filter(working_days__contains=day).last()
		return schdule
	
	def get_available_slots(self, service_id):
		from booking.utils import get_booked_slots

		booking_date = 	datetime.today()
		schdule = self.get_schdule()
		start_time = schdule.start_time
		end_time = schdule.end_time
		time_slots = []
		service = self.services.filter(id=service_id).last()
		service_time = service.time
		booked_slots = get_booked_slots(booking_date, self.id)
		while start_time < end_time:
			time_slots.append(start_time)
			start_time = (datetime.combine(date.today(), start_time) + timedelta(minutes=30)).time()
		available_slots = list(set(time_slots) - set(booked_slots))
		available_slots.sort()
		if service_time > 30:
			slots = []
			required_slot_for_service = math.ceil(service_time/30) - 1 
			for i in range(required_slot_for_service,len(available_slots)):
				start_time = (datetime.combine(date.today(), available_slots[i]) - timedelta(minutes=30*required_slot_for_service)).time()
				if start_time == available_slots[i-required_slot_for_service]:
					slots.append(available_slots[i-required_slot_for_service])
			available_slots = slots
		available_slots = [slot.strftime("%H:%M") for slot in available_slots]
		return available_slots
		

class Service(models.Model):
	name = models.CharField(max_length=50, null=False)
	time = models.IntegerField(null=False)
	price = models.IntegerField(null=False)
	saloon = models.ForeignKey(Saloon, related_name = 'services', on_delete=models.CASCADE)


class Schdule(models.Model):
	working_days = jsonfield.JSONField()#models.CharField(max_length=70,choices = SERVICE_CHOICES, null=False)
	start_time = models.TimeField()
	end_time = models.TimeField()
	saloon = models.ForeignKey(Saloon, related_name = 'schdules', on_delete=models.CASCADE)
	# is_active = models.BooleanField(default=False)