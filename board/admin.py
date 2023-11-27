from django.contrib import admin
from .models import Board

#게시판
class BoardAdmin(admin.ModelAdmin):
    list_display = ('customer', 'title', 'content', 'category', 'views_count', 'created_at')
    list_filter = ('customer', 'category',)
    
admin.site.register(Board, BoardAdmin)