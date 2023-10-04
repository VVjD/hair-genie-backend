from django.contrib import admin
from .models import Reservation

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('customer', 'salon', 'date', 'time', 'service', 'status', 'created')
    list_filter = ('date', 'salon', 'status')

admin.site.register(Reservation, ReservationAdmin)
