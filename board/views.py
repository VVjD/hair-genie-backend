from rest_framework import generics
from .models import Board
from .serializers import BoardSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view

class BoardListCreateView(generics.ListCreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    
@api_view(['GET'])
def category_list(request):
    categories = ['자유 게시판', '미용실 등록 요청']  # 실제 카테고리 목록을 여기에 추가
    
    return Response(categories)