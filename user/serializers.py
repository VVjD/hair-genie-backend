from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):

  def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = super(UserSerializer, self).create(validated_data)
        return user

  class Meta:
    model = User
    fields = ('id', 
              'uid', 
              'password', 
              'uname', 
              'unickname', 
              'uphone', 
              'uemail', 
              'signuptime')
    extra_kwargs = {'password': {'write_only': True}} # 비밀번호는 응답 x