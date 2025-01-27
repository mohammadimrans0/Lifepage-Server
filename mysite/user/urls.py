from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet, SignupViewSet, UserLoginApiView, UserLogoutApiView, ResetPasswordView

router = DefaultRouter()
router.register('profiles', ProfileViewSet, basename='profile')
router.register('signup', SignupViewSet, basename='signup')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', UserLoginApiView.as_view(), name='login'),
    path('logout/', UserLogoutApiView.as_view(), name='logout'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
]
