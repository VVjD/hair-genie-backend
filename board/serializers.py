from rest_framework import serializers
from .models import Board, Comment

class BoardSerializer(serializers.ModelSerializer):
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = '__all__'

    def get_comment_count(self, obj):
        all_comments_count = Comment.objects.filter(board=obj).count()
        return all_comments_count

class CommentSerializer(serializers.ModelSerializer):
    user_profile_image = serializers.CharField(source='customer.profile_image', read_only=True)
    user_name = serializers.CharField(source='customer.unickname', read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'

    def get_replies(self, obj):
        # 대댓글 가져오기
        replies = Comment.objects.filter(parent_comment=obj)
        serializer = CommentSerializer(replies, many=True)
        return serializer.data