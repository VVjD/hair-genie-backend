from rest_framework import generics
from .models import Board
from .serializers import BoardSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view

class BoardListCreateView(generics.ListCreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    
class BoardRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer