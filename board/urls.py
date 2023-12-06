from django.urls import path
from . import views

urlpatterns = [
    path('', views.BoardListCreateView.as_view(), name='board'),
    path('<int:pk>/', views.BoardRetrieveUpdateDestroyView.as_view(), name='board-detail'),
]