from django.urls import path
from . import views

urlpatterns = [
    path('', views.ReservationListCreateView.as_view(), name='reservation-list'),
    path('<int:pk>/', views.ReservationDetailUpdateDestroyView.as_view(), name='reservation-detail'),
    path('customer/<int:customer_id>/', views.CustomerReservationListView.as_view(), name='customer-detail'),
    path('<int:reservation_id>/cancel/', views.cancel_reservation, name='cancel-reservation'),
    path('<int:reservation_id>/complete/', views.complete_reservation, name='complete-reservation'),
    path('<int:reservation_id>/review/', views.review_reservation, name='review-reservation'),
    path('<str:hid>/review/', views.ReviewListCreateView.as_view(), name='review'),
    path('review/<int:review_number>/', views.ReviewDetailUpdateDestroyView.as_view(), name='review-detail'),
    path('review/<int:review_number>/update/', views.update_review, name='update-review'),
    path('review/<int:review_number>/delete/', views.delete_review, name='delete-review'),
]
