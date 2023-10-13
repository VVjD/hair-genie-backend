from django.urls import path
from . import views

urlpatterns = [
  path('analyze_face/', views.AnalyzeFaceShape.as_view(), name='analyze_face'),
]