from django.db import models
from hairsalon.models import Hairsalon, HairsalonService
from user.models import User
from django.utils import timezone
from datetime import datetime, time
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator

#예약
class Reservation(models.Model):
    STATUS_CHOICES = (
        ('예약 중', '예약 중'),
        ('이용 완료', '이용 완료'),
        ('예약 취소', '예약 취소'),
        ('리뷰 작성 완료', '리뷰 작성 완료'), 
    )

    customer = models.ForeignKey(User, on_delete=models.CASCADE) 
    salon = models.ForeignKey(Hairsalon, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.CharField(max_length=10)
    service = models.ForeignKey(HairsalonService, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='예약 중')
    created = models.DateTimeField(auto_now_add=True)
    
    def cancel_reservation(self):
        if self.status == '예약 중':
            self.status = '예약 취소'
            self.save()
            
    def complete_reservation(self):
        current_time = timezone.now()
        reservation_datetime = timezone.make_aware(datetime.combine(self.date, time.fromisoformat(self.time)))
        
        if current_time > reservation_datetime and self.status == '예약 중':
            self.status = '이용 완료'
            self.save()
            
    def review_reservation(self):
        if self.status == '이용 완료':
            self.status = '리뷰 작성 완료'
            self.save()
            
    def __str__(self):
        return f"[{self.customer.uname}] {self.status}- {self.salon.HName}, {self.date} {self.time} {self.service}"

    class Meta:
        db_table = "Reservation"

#리뷰    
class Review(models.Model):
    review_number = models.AutoField(primary_key=True)
    salon = models.ForeignKey(Hairsalon, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    content = models.TextField(max_length=400)
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    rating = models.IntegerField(
        choices=RATING_CHOICES,
        default=5
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def clean(self):
        if self.reservation.status not in ['이용 완료', '리뷰 작성 완료']:
            raise ValidationError('리뷰 작성은 예약 상태가 "이용 완료"인 예약에 대해서만 허용됩니다.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"Review #{self.review_number} for {self.salon.HName} by {self.customer.uname}"

    class Meta:
        db_table = "Review"