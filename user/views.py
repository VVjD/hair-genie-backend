from django.shortcuts import render
from .serializers import UserSerializer, PasswordResetSerializer
from .models import User
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

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
        
# 비밀번호 재설정 - 이메일 전송
class PasswordResetView(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            uname = serializer.validated_data['uname']
            uid = serializer.validated_data['uid']

            # 사용자 검색
            try:
                user = User.objects.get(email=email, uid=uid, uname=uname)
            except User.DoesNotExist:
                return Response({'error': '사용자를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

            # 비밀번호 재설정 링크 생성
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_link = f'http://localhost:3000/user/reset/{uidb64}/{token}/'

            # 비밀번호 재설정 이메일 보내기
            email_subject = '헤어 지니(Hair Genie) 비밀번호 재설정'
            html_message = render_to_string('password/password_reset_email.html', {
                                            'reset_link': reset_link,
                                            'user_id': user.uid
                                        })
            plain_message = strip_tags(html_message)  # HTML 태그 제거

            # 이메일 전송
            email = EmailMultiAlternatives(email_subject, plain_message, to=[email])
            email.attach_alternative(html_message, "text/html")
            email.send()

            return Response({'message': '비밀번호 재설정을 위한 링크가 이메일로 전송되었습니다.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 비밀번호 재설정
class PasswordResetConfirmView(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and default_token_generator.check_token(user, token):
            # 비밀번호 초기화 링크가 유효한 경우
            return Response({'message': '비밀번호 초기화 링크가 유효합니다. 새로운 비밀번호를 입력해주세요.'}, status=status.HTTP_200_OK)
        else:
            # 링크가 유효하지 않은 경우
            return Response({'error': '비밀번호 초기화 링크가 만료되었거나 올바르지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        
    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and default_token_generator.check_token(user, token):
            # 비밀번호 초기화 링크가 유효한 경우
            password = request.data.get('new_password')
            user.set_password(password)  # 새로운 비밀번호로 변경
            user.save()  # 변경된 비밀번호를 저장

            return Response({'message': '비밀번호가 성공적으로 변경되었습니다.'}, status=status.HTTP_200_OK)
        else:
            # 링크가 유효하지 않은 경우
            return Response({'error': '비밀번호 초기화 링크가 만료되었거나 올바르지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)

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
        
# 비밀번호 변경
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def change_password(request):
    current_password = request.data.get('current_password', '')
    new_password = request.data.get('new_password', '')
    user = request.user

    # 현재 비밀번호 검증
    if not user.check_password(current_password):
        return Response({'message': '기존 비밀번호가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)

    # 새로운 비밀번호 설정
    user.set_password(new_password)
    user.save()

    return Response({'message': '비밀번호가 성공적으로 변경되었습니다.'}, status=status.HTTP_200_OK)

# 탈퇴
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_account(request):
    user = request.user
    password = request.data.get('password', '')

    if not user.check_password(password):
        return Response({'message': '비밀번호가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user.delete()
        return Response({'message': '회원 탈퇴가 성공적으로 처리되었습니다.'}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)