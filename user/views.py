from django.shortcuts import render
from .serializers import UserSerializer
from .models import User
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
import json

# Create your views here.
class ListUser(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class DetailUser(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        try:
            # 요청 데이터를 JSON 형식으로 파싱
            data = json.loads(request.body)
            userId = data.get('uid')
            password = data.get('password')
            # 데이터를 확인하기 위해 로그로 출력
            print('userId:', userId)
            print('password:', password)
            if not userId:
                return JsonResponse({'success': False, 'error': '아이디를 입력하세요.(back)'})
            if not password:
                return JsonResponse({'success': False, 'error': '비밀번호를 입력하세요.(back)'})
            try:
                user = User.objects.get(uid=userId)
                # 평문 비밀번호를 비교
                if check_password(password, user.password):
                    login(request, user)
                    # 토큰 생성 및 반환
                    token, _ = Token.objects.get_or_create(user=user)
                    return JsonResponse({'success': True, 'token': token.key})
                else:
                    return JsonResponse({'success': False, 'error': '로그인 실패 메시지'})
            except User.DoesNotExist:
                return JsonResponse({'success': False, 'error': '아이디가 존재하지 않습니다.(back)'})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': '올바른 JSON 데이터를 제공하세요.(back)'})
    else:
        return JsonResponse({'success': False, 'error': '올바른 요청이 아닙니다.(back)'})
    
 #로그인 기록 남는 코드
''' @csrf_exempt
def login_view(request):
    if request.method == 'POST':
        try:
            # 요청 데이터를 JSON 형식으로 파싱
            data = json.loads(request.body)
            userId = data.get('uid')
            password = data.get('password')
            # 데이터를 확인하기 위해 로그로 출력
            print('userId:', userId)
            print('password:', password)
            if not userId:
                return JsonResponse({'success': False, 'error': '아이디를 입력하세요.(back)'})
            if not password:
                return JsonResponse({'success': False, 'error': '비밀번호를 입력하세요.(back)'})
            try:
                user = User.objects.get(uid=userId)
            except User.DoesNotExist:
                return JsonResponse({'success': False, 'error': '아이디가 존재하지 않습니다.(back)'})
            if user.password == password:
                login(request, user)
                print('로그인 상태:', request.user.is_authenticated)
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': '비밀번호가 올바르지 않습니다.(back)'})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': '올바른 JSON 데이터를 제공하세요.(back)'})
    else:
        return JsonResponse({'success': False, 'error': '올바른 요청이 아닙니다.(back)'}) '''

def logout_view(request):
    logout(request)
    return JsonResponse({'success': True, 'message': '로그아웃되었습니다.'})

@login_required
def check_login(request):
    return JsonResponse({'isLoggedIn': True})

class CheckUserIdExists(APIView):
    def get(self, request):
        uid = request.query_params.get('uid')

        try:
            user = User.objects.get(uid=uid)
            return Response({'exists': True}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'exists': False}, status=status.HTTP_200_OK)
