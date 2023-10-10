from django.urls import path
from . import views

urlpatterns = [
    path('analyze-face/', views.analyze_face, name='analyze_face'),
]
