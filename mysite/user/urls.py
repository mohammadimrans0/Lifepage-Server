from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CheckFollowStatusView, UserFollowView, UserProfileViewSet, SignupViewSet, UserLoginApiView, UserLogoutApiView, ResetPasswordView

router = DefaultRouter()
router.register('profiles', UserProfileViewSet, basename='profile')
router.register('signup', SignupViewSet, basename='signup')

urlpatterns = [
    path('', include(router.urls)),
    path('follow/', UserFollowView.as_view(), name='follow'),
     path('follow/status/', CheckFollowStatusView.as_view(), name='check_follow_status'),
    path('login/', UserLoginApiView.as_view(), name='login'),
    path('logout/', UserLogoutApiView.as_view(), name='logout'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
]
