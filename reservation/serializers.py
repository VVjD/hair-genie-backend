from rest_framework import serializers
from .models import Reservation

class ReservationSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=Reservation.STATUS_CHOICES, read_only=True)

    class Meta:
        model = Reservation
        fields = ('id', 'customer', 'salon', 'date', 'time', 'service', 'status', 'created')