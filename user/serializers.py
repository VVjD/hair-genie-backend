from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):

  def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        profile_image = validated_data.pop('profile_image', None)
        user = super(UserSerializer, self).create(validated_data)

        if not profile_image:
            user.profile_image = 'profile_imgs/default.png'
            user.save()
        
        return user

  class Meta:
    model = User
    fields = ('id', 
              'uid', 
              'password', 
              'uname', 
              'unickname',
              'profile_image',
              'face_shape',
              'uphone', 
              'email', 
              'signuptime')
    extra_kwargs = {'password': {'write_only': True}} # 비밀번호는 응답 x

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    uname = serializers.CharField()
    uid = serializers.CharField()