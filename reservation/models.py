from django.db import models
from user.models import User
from hairsalon.models import Hairsalon, Service  # Service 모델 추가

class Reservation(models.Model):
    RNum = models.AutoField(primary_key=True)  # AutoField를 사용하여 자동으로 생성되도록 변경
    RDate = models.DateField()
    RTime = models.TimeField()
    UID = models.ForeignKey(User, on_delete=models.CASCADE)
    HID = models.ForeignKey(Hairsalon, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    class Meta:
        db_table = "Reservation"