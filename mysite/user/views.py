from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Profile, Follow
from .serializers import SignupSerializer, ProfileSerializer, FollowSerializer, UserSerializer, UserLoginSerializer, ResetPasswordSerializer
from django.contrib.auth import login, logout
from rest_framework.authtoken.models import Token

# user viewset
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    

# profile viewset
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
    

# follow view
class FollowView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            following_id = request.data.get('following_id')
            following = Profile.objects.get(id=following_id)
            follower = request.user.profile

            # Prevent self-follow
            if follower == following:
                return Response({"error": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

            # Check if already following
            if Follow.objects.filter(follower=follower, following=following).exists():
                return Response({"error": "Already following this user."}, status=status.HTTP_400_BAD_REQUEST)

            follow = Follow.objects.create(follower=follower, following=following)
            serializer = FollowSerializer(follow)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except Profile.DoesNotExist:
            return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        following_id = request.data.get('following_id')
        follower = request.user.profile

        try:
            following = Profile.objects.get(id=following_id)
            follow_instance = Follow.objects.get(follower=follower, following=following)
            follow_instance.delete()
            return Response({"message": "Unfollowed successfully."}, status=status.HTTP_204_NO_CONTENT)

        except Profile.DoesNotExist:
            return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        except Follow.DoesNotExist:
            return Response({"error": "You are not following this user."}, status=status.HTTP_400_BAD_REQUEST)


# signup user
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
