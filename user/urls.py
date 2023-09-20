from django.urls import path

from . import views

urlpatterns = [
  path('', views.ListUser.as_view()),
  path('<int:pk>/', views.DetailUser.as_view()),
  path('login/', views.login_view, name='login'),
  path('logout/', views.logout_view, name='logout'),
  path('check_login/', views.check_login, name='check_login'),
  path('check-id-exists/', views.CheckUserIdExists.as_view()),
  path('find-userid/', views.FindUserId.as_view()),
  path('find-userpw/', views.FindUserPw.as_view()),
]