from django.urls import path
from . import views

urlpatterns = [
    path('', views.ReservationListCreateView.as_view(), name='reservation-list'),
    path('<int:pk>/', views.ReservationDetailUpdateDestroyView.as_view(), name='reservation-detail'),
    path('customer/<int:customer_id>/', views.CustomerReservationListView.as_view(), name='customer-detail'),
    path('<int:reservation_id>/cancel/', views.cancel_reservation, name='cancel-reservation'),
    path('<int:reservation_id>/complete/', views.complete_reservation, name='complete-reservation'),
]
