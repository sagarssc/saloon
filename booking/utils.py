from .models import Booking
from registration.models import Saloon, Service
from datetime import datetime, date, time, timedelta

def get_booked_slots(booking_date, saloon_id):
	slots = {}
	booked_slots = []
	bookings = Booking.objects.filter(booking_date=booking_date, saloon_id=saloon_id)
	saloon = bookings.last().saloon
	for booking in bookings:
		slot = booking.start_time
		while slot < booking.end_time:
			start_time = slot
			if start_time in slots:
				slots[start_time] += 1
			else:
				slots[start_time] = 1
			slot = (datetime.combine(date.today(), slot) + timedelta(minutes=30)).time()
	booked_slots = [slot for slot,count in slots.items() if count == saloon.no_of_sheets]
	return booked_slots

def get_all_slots(service_id):
	services = Service.objects.filter(id=service_id)
	saloons = []
	for service in services:
		saloon = service.saloon
		schdule = saloon.get_schdule()
		data = {
			"saloon_name": saloon.name,
			"address": saloon.address,
			"available_slots": saloon.get_available_slots(service_id),
			"opens_at": schdule.start_time,
			"closes_at":schdule.end_time
		}
		saloons.append(data)
	return saloons