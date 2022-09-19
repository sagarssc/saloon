from django.contrib import admin

from .models import Booking

class BookingAdmin(admin.ModelAdmin):
	list_display = (
			'booking_date',
			'start_time',
			'end_time',
			'price',
			'get_cutomer',
			'get_saloon',
			'get_service',
			'is_cancelled',
		)

	def get_cutomer(self, obj):
		return obj.customer.username

	def get_saloon(self, obj):
		return obj.saloon.name

	def get_service(self, obj):
		return obj.service.name

admin.site.register(Booking, BookingAdmin)
