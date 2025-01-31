from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
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

    def create(self, request, *args, **kwargs):
        user = request.data.get('user')
        post = request.data.get('post')

        if LikePost.objects.filter(user=user, post=post).exists():
            return Response(
                {"detail": "You have already liked this post."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().create(request, *args, **kwargs)

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

    def create(self, request, *args, **kwargs):
        user = request.data.get('user')
        post = request.data.get('post')

        if BookMark.objects.filter(user=user, post=post).exists():
            return Response(
                {"detail": "You have already bookmarked this post."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().create(request, *args, **kwargs)
