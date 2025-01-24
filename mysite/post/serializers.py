from rest_framework import serializers
from .models import Post, LikePost, CommentPost, BookMark

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

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
