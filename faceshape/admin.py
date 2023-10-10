from django.contrib import admin
from .models import FaceAnalysisResult

@admin.register(FaceAnalysisResult)
class FaceAnalysisResultAdmin(admin.ModelAdmin):
    list_display = ('face_type', 'probability', 'created_at')
    list_filter = ('face_type', 'created_at')
    search_fields = ('face_type',)
    ordering = ('-created_at',)
