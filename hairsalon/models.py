from django.db import models

class Hairsalon(models.Model):
    HID = models.CharField(max_length=50, primary_key=True)
    HName = models.CharField(max_length=100)
    HLoc = models.CharField(max_length=200)
    
    def __str__(self):
        return self.HName
    
    class Meta:
        db_table = "Hairsalon"
    
class HairsalonService(models.Model):
    salon = models.ForeignKey(Hairsalon, related_name='services', on_delete=models.CASCADE)
    menu_name = models.CharField(max_length=20, choices=[('컷', '컷'), ('펌', '펌'), ('컬러', '컬러'), ('클리닉', '클리닉')])
    service_name = models.CharField(max_length=100) 
    price = models.CharField(max_length=10) 

    def __str__(self):
        return self.service_name
    
    class Meta:
        db_table = "HairsalonService"