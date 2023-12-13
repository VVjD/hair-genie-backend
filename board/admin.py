from django.contrib import admin
from .models import Board, Comment

class BoardAdmin(admin.ModelAdmin):
    list_display = ('customer', 'category', 'title', 'content', 'views_count', 'created_at')
    list_filter = ('customer','category')

admin.site.register(Board, BoardAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'board', 'customer', 'comment', 'created_at')
    list_filter = ('id', 'board')

admin.site.register(Comment, CommentAdmin)