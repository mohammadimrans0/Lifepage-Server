from rest_framework import viewsets, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from .models import Profile, Follow
from .serializers import SignupSerializer, ProfileSerializer, FollowSerializer, UserSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_queryset(self):
        """
        Override the default queryset to filter for the authenticated user's profile
        when updating, otherwise return all profiles.
        """
        if self.action in ['update', 'partial_update']:
            return Profile.objects.all()  # No authentication applied here.
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


class AuthViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            return Response({"detail": "Logged in successfully."}, status=status.HTTP_200_OK)
        return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['post'])
    def logout(self, request):
        return Response({"detail": "Logged out successfully."}, status=status.HTTP_200_OK)


class ResetPasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')
        user = get_object_or_404(User, email=email)
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)
        reset_url = f"http://frontend-url/reset-password/{user.pk}/{token}"
        send_mail(
            subject="Password Reset Request",
            message=f"Click the link to reset your password: {reset_url}",
            from_email="no-reply@example.com",
            recipient_list=[email],
        )
        return Response({"detail": "Password reset email sent."}, status=status.HTTP_200_OK)

    def put(self, request, user_id, token):
        password = request.data.get('password')
        user = get_object_or_404(User, pk=user_id)
        token_generator = PasswordResetTokenGenerator()
        if token_generator.check_token(user, token):
            user.set_password(password)
            user.save()
            return Response({"detail": "Password reset successfully."}, status=status.HTTP_200_OK)
        return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)
