from rest_framework import generics
from .models import Board, Comment
from .serializers import BoardSerializer, CommentSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.core.exceptions import PermissionDenied

class BoardListCreateView(generics.ListCreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    def get_queryset(self):
        queryset = Board.objects.annotate(comment_count=Count('comments'))
        return queryset
    
    #관리자만 공지 작성할 수 있게 설정
    def perform_create(self, serializer):
        if self.request.data.get('category') == '공지':
            if not self.request.user.is_staff:  # 관리자 권한 확인
                raise PermissionDenied("공지는 관리자만 작성할 수 있습니다.")
        serializer.save()
    
class BoardRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    
#조회수
class IncrementViews(APIView):
    def put(self, request, pk):
        try:
            # 게시글 가져오기
            board = Board.objects.get(pk=pk)
            
            # 조회수 증가
            board.views_count += 1
            board.save()
            
            # 증가된 조회수와 함께 게시글 정보 반환
            return Response({'views_count': board.views_count}, status=status.HTTP_200_OK)
        
        except Board.DoesNotExist:
            return Response({'message': 'Board not found'}, status=status.HTTP_404_NOT_FOUND)
        
# 댓글 조회/작성
class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        board_id = self.kwargs['pk']
        return Comment.objects.filter(board_id=board_id)
    
# 댓글 수정/삭제
class CommentUpdateView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        board_id = self.kwargs['pk']
        comment_id = self.kwargs['comment_id']
        return Comment.objects.filter(board_id=board_id, id=comment_id)
    
    def get_object(self):
        board_id = self.kwargs['pk']
        comment_id = self.kwargs['comment_id']
        return get_object_or_404(Comment, board_id=board_id, id=comment_id)
    
#사용자 댓글 모아보기
class UserCommentsListView(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Comment.objects.filter(customer=user_id)
    