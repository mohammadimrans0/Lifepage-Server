from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ProfileViewSet, FollowView, SignupViewSet, UserLoginApiView, UserLogoutApiView, ResetPasswordView

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('profiles', ProfileViewSet, basename='profile')
router.register('signup', SignupViewSet, basename='signup')

urlpatterns = [
    path('', include(router.urls)),
    path('follow/', FollowView.as_view(), name='follow'),
    path('login/', UserLoginApiView.as_view(), name='login'),
    path('logout/', UserLogoutApiView.as_view(), name='logout'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
]
