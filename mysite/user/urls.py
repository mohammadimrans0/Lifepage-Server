from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet, SignupViewSet, AuthViewSet, ResetPasswordView

router = DefaultRouter()
router.register('profiles', ProfileViewSet, basename='profile')
router.register('signup', SignupViewSet, basename='signup')
router.register('auth', AuthViewSet, basename='auth')

urlpatterns = [
    path('', include(router.urls)),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
]
