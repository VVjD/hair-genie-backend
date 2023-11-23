from django.db import models

class Hairsalon(models.Model):
    HID = models.CharField(max_length=50, primary_key=True)
    HName = models.CharField(max_length=100)
    HLoc = models.CharField(max_length=200)
    REGION_CHOICES = [
        ('서울', '서울'),
        ('부산', '부산'),
        ('대구', '대구'),
        ('인천', '인천'),
        ('광주', '광주'),
        ('대전', '대전'),
        ('울산', '울산'),
        ('세종', '세종'),
        ('경기', '경기'),
        ('강원', '강원'),
        ('충북', '충북'),
        ('충남', '충남'),
        ('전북', '전북'),
        ('전남', '전남'),
        ('경북', '경북'),
        ('경남', '경남'),
        ('제주', '제주'),
    ]
    HRegion = models.CharField(max_length=20, choices=REGION_CHOICES)
    HPhone = models.CharField(max_length=15, default='00-000-0000') #한 번 마이그레이션 후 default 삭제
    
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
