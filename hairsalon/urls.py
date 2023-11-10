from django.urls import path
from . import views

urlpatterns = [
    path('', views.HairsalonListCreateView.as_view(), name='hairsalon-list'),
    path('<str:pk>/', views.HairsalonDetailUpdateDestroyView.as_view(), name='hairsalon-detail'),
    path('<str:hid>/service/', views.HairsalonServiceListView.as_view(), name='service-list'),
    path('service/<int:pk>/', views.HairsalonServiceDetailUpdateDestroyView.as_view(), name='service-detail'),
] 