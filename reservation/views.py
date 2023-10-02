from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Reservation
from rest_framework.views import APIView
from .serializers import ReservationSerializer

class ReservationListCreateView(generics.ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

class ReservationDetailUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

# customer_id를 기반으로 해당 customer의 예약 목록을 필터링
class CustomerReservationListView(generics.ListAPIView):
    serializer_class = ReservationSerializer

    def get_queryset(self):
        customer_id = self.kwargs['customer_id']
        queryset = Reservation.objects.filter(customer_id=customer_id)
        return queryset
    
#예약 취소
@api_view(['PUT'])
def cancel_reservation(request, reservation_id):
    reservation = Reservation.objects.filter(id=reservation_id).first()
    
    if not reservation:
        return Response({'message': '예약을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'PUT':
        reservation.cancel_reservation()
        return Response({'message': '예약이 취소되었습니다.'})
    
    return Response({'message': '예약 취소 요청은 PUT 메서드로 보내야 합니다.'}, status=status.HTTP_400_BAD_REQUEST) 

# 예약 완료
@api_view(['PUT'])
def complete_reservation(request, reservation_id):
    reservation = Reservation.objects.filter(id=reservation_id).first()

    if not reservation:
        return Response({'message': '예약을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        reservation.complete_reservation()
        return Response({'message': '예약이 이용 완료되었습니다.'})
    
    return Response({'message': '예약 완료 요청은 PUT 메서드로 보내야 합니다.'}, status=status.HTTP_400_BAD_REQUEST)
