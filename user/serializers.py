from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
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