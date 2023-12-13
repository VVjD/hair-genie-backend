from django.db import models
from user.models import User

class Board(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE) 
    CATEGORY_CHOICES = [
        ('공지', '공지'),
        ('자유', '자유'),
        ('미용실 등록 요청', '미용실 등록 요청'),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=200)
    content = models.TextField()
    views_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = "Board"

class Comment(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='comments')
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment
    
    class Meta:
        db_table = "Comment"