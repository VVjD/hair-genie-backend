from rest_framework import serializers
from .models import Reservation, Review

class ReservationSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=Reservation.STATUS_CHOICES, read_only=True)
    class Meta:
        model = Reservation
        fields = ('id', 'customer', 'salon', 'date', 'time', 'service', 'status', 'created')
        
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('review_number', 'salon', 'customer', 'reservation', 'content', 'created_at')