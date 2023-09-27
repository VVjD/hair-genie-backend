from rest_framework import serializers
from .models import Hairsalon, HairsalonService

class HairsalonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hairsalon
        fields = ('HID', 'HName', 'HLoc')

class HairsalonServiceSerializer(serializers.ModelSerializer):
    # Hairsalon 모델의 필드를 정의합니다.
    salon_HID = serializers.CharField(source='salon.HID', read_only=True)

    class Meta:
        model = HairsalonService
        fields = ('id', 'salon', 'salon_HID', 'menu_name', 'service_name', 'price')