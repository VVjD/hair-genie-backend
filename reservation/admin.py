from django.contrib import admin
from .models import Reservation, Review

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('customer', 'salon', 'date', 'time', 'service', 'status', 'created')
    list_filter = ('date', 'salon', 'status')

admin.site.register(Reservation, ReservationAdmin)

#리뷰
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('review_number', 'salon', 'customer', 'reservation', 'content', 'created_at')
    list_filter = ('salon', 'customer')
    
admin.site.register(Review, ReviewAdmin)