from rest_framework import serializers
from .models import Post, LikePost, CommentPost, BookMark

class PostSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    class Meta:
        model = Post
        fields = ['id', 'user', 'image', 'caption', 'no_of_likes', 'no_of_comments', 'created_at']

class LikePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikePost
        fields = '__all__'

class CommentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentPost
        fields = '__all__'

class BookMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookMark
        fields = '__all__'
