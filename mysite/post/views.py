from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post, LikePost, CommentPost, BookMark
from .serializers import PostSerializer, LikePostSerializer, CommentPostSerializer, BookMarkSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user']

class LikePostViewSet(viewsets.ModelViewSet):
    queryset = LikePost.objects.all()
    serializer_class = LikePostSerializer

class CommentPostViewSet(viewsets.ModelViewSet):
    queryset = CommentPost.objects.all()
    serializer_class = CommentPostSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['post']

class BookMarkViewSet(viewsets.ModelViewSet):
    queryset = BookMark.objects.all()
    serializer_class = BookMarkSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user']
