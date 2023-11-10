from django.urls import path
from . import views

urlpatterns = [
  path('hair_synthesis/', views.HairSynthesis.as_view(), name='hair_synthesis'),
]