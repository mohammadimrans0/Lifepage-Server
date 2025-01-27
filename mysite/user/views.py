from rest_framework import viewsets, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import authenticate
# from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from .models import Profile, Follow
from .serializers import SignupSerializer, ProfileSerializer, FollowSerializer, UserSerializer, UserLoginSerializer, ResetPasswordSerializer
from django.contrib.auth import login, logout
from rest_framework.authtoken.models import Token


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_queryset(self):
        if self.action in ['update', 'partial_update']:
            return Profile.objects.all()
        return super().get_queryset()

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=['post'])
    def follow(self, request, pk=None):
        """Follow a profile."""
        profile = self.get_object()
        Follow.objects.get_or_create(
            follower=None,  # Replace None with proper user logic later.
            following=profile
        )
        return Response({"detail": "Followed successfully"}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def unfollow(self, request, pk=None):
        """Unfollow a profile."""
        profile = self.get_object()
        follow_instance = Follow.objects.filter(follower=None, following=profile)  # Replace None with user logic later.
        if follow_instance.exists():
            follow_instance.delete()
            return Response({"detail": "Unfollowed successfully"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "You are not following this profile."}, status=status.HTTP_400_BAD_REQUEST)


class SignupViewSet(viewsets.ViewSet):
    serializer_class = SignupSerializer

    def create(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"detail": "User created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Login user
class UserLoginApiView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username=username, password=password)
            
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                login(request, user)
                return Response({'token': token.key, 'user_id': user.id})
            else:
                return Response({'error': "Invalid Username or Password"})
        return Response(serializer.errors)


# Logout user
class UserLogoutApiView(APIView):
    def post(self, request):
        if hasattr(request.user, 'auth_token'):
            request.user.auth_token.delete()
        logout(request)
        return Response({"message": "Logout successful."})


# reset password
class ResetPasswordView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password reset successful."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
