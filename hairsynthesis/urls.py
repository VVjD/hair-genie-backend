from django.urls import path
from . import views

app_name = 'hairsynthesis'

urlpatterns = [
    path('hairsynthesis/', views.hairsynthesis, name='hairsynthesis'),  # 헤어스타일 합성 페이지 URL 패턴
    #path('hairsynthesis/result/', views.hair_synthesis_result, name='hair_synthesis_result'),  # 합성 결과 출력 페이지 URL 패턴
]
