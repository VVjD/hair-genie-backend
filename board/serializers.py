from rest_framework import serializers
from .models import Board, Comment

class BoardSerializer(serializers.ModelSerializer):
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = '__all__'

    def get_comment_count(self, obj):
        return obj.comments.count()

class CommentSerializer(serializers.ModelSerializer):
    user_profile_image = serializers.CharField(source='customer.profile_image', read_only=True)
    user_name = serializers.CharField(source='customer.unickname', read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'