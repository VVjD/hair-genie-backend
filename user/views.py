from django.shortcuts import render
from .serializers import UserSerializer
from .models import User
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
class ListUser(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class DetailUser(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# 아이디 중복 확인
class CheckUserIdExists(APIView):
    def get(self, request):
        uid = request.query_params.get('uid')

        try:
            user = User.objects.get(uid=uid)
            return Response({'exists': True}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'exists': False}, status=status.HTTP_200_OK)

# 사용자 아이디 찾기
class FindUserId(APIView):
    def get(self, request):
        uname = request.query_params.get('uname')
        uphone = request.query_params.get('uphone')

        try:
            user = User.objects.get(uname=uname, uphone=uphone)
            serializer = UserSerializer(user)
            return Response({"uid": serializer.data['uid']}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"message": "사용자를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

# 사용자 비밀번호 찾기
class FindUserPw(APIView):
    def get(self, request):
        uname = request.query_params.get('uname')
        uid = request.query_params.get('uid')
        uphone = request.query_params.get('uphone')

        try:
            user = User.objects.get(uname=uname, uid=uid, uphone=uphone)
            serializer = UserSerializer(user)
            return Response({"password": serializer.data['password']}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"mesersage": "사용자를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)