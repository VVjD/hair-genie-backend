from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
  TokenObtainPairView, 
  TokenRefreshView,
)

urlpatterns = [
  path('', views.ListUser.as_view(), name='list'),
  path('<int:pk>/', views.DetailUser.as_view(), name='detail'),
  # 회원가입
  path('join/', views.Join.as_view(), name='join'),
  # 아이디 중복
  path('check-id-exists/', views.CheckUserIdExists.as_view(), name='check-id-exists'),
  # id 찾기
  path('find-userid/', views.FindUserId.as_view(), name='find-userid'),
  # pw 찾기
  path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
  # path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
  path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
  # path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
  # 토큰
  path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
  # 사용자 정보
  path('info/', views.user_info, name='user_info'),
  # 비밀번호 변경
  path('change_password/', views.change_password, name='change_password'),
  # 탈퇴
  path('delete_account/', views.delete_account, name='delete_account'),
]