from django.contrib import admin

from . models import Signal
from . models import Client

class ClientAdmin(admin.ModelAdmin):
	list_display = ('email', 'telegram', 'slack')

class SignalAdmin(admin.ModelAdmin):
	list_display = ('pair', 'period', 'time', 'action')

admin.site.register(Signal, SignalAdmin)
admin.site.register(Client, ClientAdmin)