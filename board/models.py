from django.db import models
from user.models import User

class Board(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE) 
    title = models.CharField(max_length=200)
    content = models.TextField()
    views_count = models.IntegerField(default=0)
    CATEGORY_CHOICES = [
        ('자유 게시판', '자유 게시판'),
        ('미용실 등록 요청', '미용실 등록 요청'),
    ]
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = "Board"