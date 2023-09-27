from django.db import models
from hairsalon.models import Hairsalon, HairsalonService
from user.models import User

class Reservation(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE) 
    salon = models.ForeignKey(Hairsalon, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.CharField(max_length=10)
    service = models.ForeignKey(HairsalonService, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.salon.HName} - {self.date} {self.time} {self.service}"

    class Meta:
        db_table = "Reservation"
