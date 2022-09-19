from django.contrib import admin

from .models import Saloon, Service, Schdule

class SaloonAdmin(admin.ModelAdmin):
	list_display = (
			'name',
			'gstin',
			'pan_no',
			'address',
			'no_of_sheets',
			'get_owner',
		)
	def get_owner(self, obj):
		return obj.owner.username

class ServiceAdmin(admin.ModelAdmin):
	list_display = (
			'name',
			'price',
			'time',
			'get_saloon',
		)
	
	def get_saloon(self, obj):
		return obj.saloon.name

class SchduleAdmin(admin.ModelAdmin):
	list_display = (
		'working_days',
		'start_time',
		'end_time',
		'get_saloon',
		)
	
	def get_saloon(self, obj):
		return obj.saloon.name


admin.site.register(Saloon, SaloonAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Schdule, SchduleAdmin)
	
	