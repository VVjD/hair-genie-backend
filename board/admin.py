from django.contrib import admin
from .models import Board

class BoardAdmin(admin.ModelAdmin):
    list_display = ('customer', 'title', 'content', 'views_count', 'created_at')
    list_filter = ('customer',)

admin.site.register(Board, BoardAdmin)
