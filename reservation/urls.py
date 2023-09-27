from django.urls import path
from . import views

urlpatterns = [
    path('', views.ReservationListCreateView.as_view(), name='reservation-list'),
    path('<int:pk>/', views.ReservationDetailUpdateDestroyView.as_view(), name='reservation-detail'),
]
