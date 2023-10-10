from django.db import models
from hairsalon.models import Hairsalon, HairsalonService
from user.models import User
from django.utils import timezone
from datetime import datetime, time

class Reservation(models.Model):
    STATUS_CHOICES = (
        ('예약 중', '예약 중'),
        ('이용 완료', '이용 완료'),
        ('예약 취소', '예약 취소'),
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
            
    def __str__(self):
        return f"{self.status} - {self.salon.HName}, {self.date} {self.time} {self.service}"

    class Meta:
        db_table = "Reservation"