from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Profile, Follow
from .serializers import SignupSerializer, FollowSerializer, UserSerializer, UserLoginSerializer, ResetPasswordSerializer
from django.contrib.auth import login, logout
from rest_framework.authtoken.models import Token

# user profile view


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# follow view
class UserFollowView(APIView):
    def post(self, request, *args, **kwargs):
        """Follow a user."""
        serializer = FollowSerializer(data=request.data)

        if serializer.is_valid():
            follow = serializer.save()  # Uses `create` method in serializer
            return Response(
                {"detail": "Following successfully.",
                    "created_at": follow.created_at},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        """Unfollow a user."""
        follower_id = request.query_params.get('follower_id')
        following_id = request.query_params.get('following_id')

        if not follower_id or not following_id:
            return Response(
                {"detail": "Both `follower_id` and `following_id` are required."},
                status=status.HTTP_400_BAD_REQUEST
        )

        try:
            follower = Profile.objects.get(id=follower_id)
            following = Profile.objects.get(id=following_id)
        except Profile.DoesNotExist:
            return Response({"detail": "Invalid user IDs provided."}, status=status.HTTP_400_BAD_REQUEST)

        follow_instance = Follow.objects.filter(
            follower=follower, following=following).first()
        if not follow_instance:
            return Response({"detail": "You are not following this user."}, status=status.HTTP_400_BAD_REQUEST)

        follow_instance.delete()
        return Response({"detail": "Unfollowed successfully."}, status=status.HTTP_204_NO_CONTENT)
    

class CheckFollowStatusView(APIView):
    def get(self, request, *args, **kwargs):
        follower_id = request.query_params.get('follower_id')
        following_id = request.query_params.get('following_id')

        # Validate query parameters
        if not follower_id or not following_id:
            return Response(
                {"detail": "Both `follower_id` and `following_id` are required."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if follow relationship exists
        is_followed = Follow.objects.filter(follower_id=follower_id, following_id=following_id).exists()

        return Response({"is_followed": is_followed}, status=status.HTTP_200_OK)


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
