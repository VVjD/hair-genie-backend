from django.shortcuts import render
from .serializers import HairsalonSerializer, HairsalonServiceSerializer
from .models import Hairsalon, HairsalonService
from rest_framework import generics

#미용실
class HairsalonListCreateView(generics.ListCreateAPIView):
    queryset = Hairsalon.objects.all()
    serializer_class = HairsalonSerializer

class HairsalonDetailUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Hairsalon.objects.all()
    serializer_class = HairsalonSerializer

#서비스
class HairsalonServiceListView(generics.ListAPIView):
    serializer_class = HairsalonServiceSerializer

    def get_queryset(self):
        hid = self.kwargs.get('hid')
        queryset = HairsalonService.objects.filter(salon__HID=hid)
        return queryset
    
class HairsalonServiceDetailUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HairsalonService.objects.all()
    serializer_class = HairsalonServiceSerializer