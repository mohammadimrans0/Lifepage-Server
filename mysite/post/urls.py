from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, LikePostViewSet, CommentPostViewSet, BookMarkViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'likepost', LikePostViewSet)
router.register(r'commentpost', CommentPostViewSet)
router.register(r'bookmarks', BookMarkViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
