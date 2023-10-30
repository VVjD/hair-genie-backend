from rest_framework import serializers
from .models import Hairsalon, HairsalonService

class HairsalonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hairsalon
        fields = ('HID', 'HName', 'HLoc', 'HRegion')

class HairsalonServiceSerializer(serializers.ModelSerializer):
    salon_HID = serializers.CharField(source='salon.HID', read_only=True)

    class Meta:
        model = HairsalonService
        fields = ('id', 'salon', 'salon_HID', 'menu_name', 'service_name', 'price')