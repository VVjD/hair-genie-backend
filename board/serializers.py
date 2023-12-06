from rest_framework import serializers
from .models import Board, Comment

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    user_profile_image = serializers.CharField(source='customer.profile_image', read_only=True)
    user_name = serializers.CharField(source='customer.unickname', read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'