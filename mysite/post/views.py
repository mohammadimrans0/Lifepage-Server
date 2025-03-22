from rest_framework import viewsets
from rest_framework.views import APIView
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
    
    def delete(self, request, *args, **kwargs):
        user_id = request.query_params.get('user_id')
        post_id = request.query_params.get('post_id')

        try:
            like_post = LikePost.objects.get(user_id=user_id, post_id=post_id)
        except LikePost.DoesNotExist:
            return Response(
                {"detail": "Like for this post by this user does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Delete the LikePost object
        like_post.delete()

        return Response(
            {"detail": "Like removed successfully."},
            status=status.HTTP_204_NO_CONTENT
        )
    

class IsLikedView(APIView):
    def get(self, request, *args, **kwargs):
        user_id = request.query_params.get('user_id')
        post_id = request.query_params.get('post_id')

        # Check if user_id and post_id are provided
        if not user_id or not post_id:
            return Response(
                {"detail": "Both `user_id` and `post_id` are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if the LikePost entry exists
        is_liked = LikePost.objects.filter(user_id=user_id, post_id=post_id).exists()

        return Response(
            {"is_liked": is_liked},
            status=status.HTTP_200_OK
        )

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
    
    def delete(self, request, *args, **kwargs):
        user_id = request.query_params.get('user_id')
        post_id = request.query_params.get('post_id')

        # Find the BookMark object matching the user and post
        try:
            bookmark = BookMark.objects.get(user_id=user_id, post_id=post_id)
        except BookMark.DoesNotExist:
            return Response(
                {"detail": "Bookmark for this post by this user does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Delete the BookMark object
        bookmark.delete()

        return Response(
            {"detail": "Bookmark removed successfully."},
            status=status.HTTP_204_NO_CONTENT
        )
    

class IsBookmarkedView(APIView):
    def get(self, request, *args, **kwargs):
        user_id = request.query_params.get('user_id')
        post_id = request.query_params.get('post_id')

        # Check if user_id and post_id are provided
        if not user_id or not post_id:
            return Response(
                {"detail": "Both `user_id` and `post_id` are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if the LikePost entry exists
        is_bookmarked = BookMark.objects.filter(user_id=user_id, post_id=post_id).exists()

        return Response(
            {"is_bookmarked": is_bookmarked},
            status=status.HTTP_200_OK
        )
