from django.shortcuts import render
from .serializers import UserSerializer
from .models import User
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class ListUser(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class DetailUser(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# 회원가입
class Join(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        
# 사용자 정보
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_info(request):
    user = request.user

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        updated_data = request.data
        serializer = UserSerializer(instance=user, data=updated_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': '사용자 정보가 업데이트되었습니다.'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)