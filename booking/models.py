from django.db import models
from django.contrib.auth.models import User
from registration.models import Saloon, Service
# Create your models here.

class Booking(models.Model):
	booking_date = models.DateField()
	start_time = models.TimeField()
	end_time = models.TimeField()
	customer = models.ForeignKey(User, related_name = 'bookings', on_delete=models.CASCADE)
	saloon = models.ForeignKey(Saloon, related_name = 'bookings', on_delete=models.CASCADE)
	service = models.ForeignKey(Service, related_name = 'bookings', on_delete=models.CASCADE)
	price = models.IntegerField(default=0)
	is_cancelled = models.BooleanField(default=False)