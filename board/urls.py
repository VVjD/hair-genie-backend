from django.urls import path
from . import views

urlpatterns = [
    path('', views.BoardListCreateView, name='post_list'),
]