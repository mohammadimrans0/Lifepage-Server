from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IsBookmarkedView, IsLikedView, PostViewSet, LikePostViewSet, CommentPostViewSet, BookMarkViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'likepost', LikePostViewSet)
router.register(r'commentpost', CommentPostViewSet)
router.register(r'bookmarks', BookMarkViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('like/status/', IsLikedView.as_view(), name='is_liked'),
    path('bookmark/status/', IsBookmarkedView.as_view(), name='is_bookmarked'),
]
