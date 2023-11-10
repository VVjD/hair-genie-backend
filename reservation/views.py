from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Reservation, Review
from rest_framework.views import APIView
from .serializers import ReservationSerializer, ReviewSerializer

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

# 이용 완료
@api_view(['PUT'])
def complete_reservation(request, reservation_id):
    reservation = Reservation.objects.filter(id=reservation_id).first()

    if not reservation:
        return Response({'message': '예약을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        reservation.complete_reservation()
        return Response({'message': '예약이 이용 완료되었습니다.'})
    
    return Response({'message': '예약 완료 요청은 PUT 메서드로 보내야 합니다.'}, status=status.HTTP_400_BAD_REQUEST)

# 리뷰 작성 완료
@api_view(['PUT'])
def review_reservation(request, reservation_id):
    reservation = Reservation.objects.filter(id=reservation_id).first()

    if not reservation:
        return Response({'message': '예약을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        reservation.review_reservation()
        return Response({'message': '리뷰 작성이 완료되었습니다.'})
    
    return Response({'message': '리뷰 작성 요청은 PUT 메서드로 보내야 합니다.'}, status=status.HTTP_400_BAD_REQUEST)

#리뷰
class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        hid = self.kwargs.get('hid')
        queryset = Review.objects.filter(salon__HID=hid)
        return queryset

class ReviewDetailUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = 'review_number'
    
# 리뷰 수정
@api_view(['PUT'])
def update_review(request, review_number):
    try:
        review = Review.objects.get(pk=review_number)
    except Review.DoesNotExist:
        return Response({'message': '리뷰를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        # 수정할 데이터를 요청에서 가져옵니다.
        content = request.data.get('content', review.content)

        # 리뷰 내용을 수정합니다.
        review.content = content
        review.save()

        return Response({'message': '리뷰가 성공적으로 수정되었습니다.'})

    return Response({'message': '리뷰 수정 요청은 PUT 메서드로 보내야 합니다.'}, status=status.HTTP_400_BAD_REQUEST)

#리뷰 삭제
@api_view(['DELETE'])
def delete_review(request, review_number):
    try:
        review = Review.objects.get(pk=review_number)
    except Review.DoesNotExist:
        return Response({'message': '리뷰를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        # 예약 상태를 '이용 완료'로 변경
        reservation = review.reservation  # 리뷰와 연결된 예약 가져오기
        if reservation:
            reservation.status = '이용 완료'
            reservation.save()

        review.delete()
        return Response({'message': '리뷰가 성공적으로 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)

    return Response({'message': '리뷰 삭제 요청은 DELETE 메서드로 보내야 합니다.'}, status=status.HTTP_400_BAD_REQUEST)
