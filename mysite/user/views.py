from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Profile, Follow
from .serializers import SignupSerializer, ProfileSerializer, FollowSerializer, UserSerializer, UserLoginSerializer, ResetPasswordSerializer
from django.contrib.auth import login, logout
from rest_framework.authtoken.models import Token

# user viewset
class UserViewSet(viewsets.ReadOnlyModelViewSet):
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
    

# follow view
class UserFollowView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = FollowSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()  # Uses `create` method in serializer
            return Response({"detail": "Following successfully."}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        follower_id = request.query_params.get('follower_id')
        following_id = request.query_params.get('following_id')

        if not follower_id or not following_id:
            return Response({"detail": "Both follower_id and following_id are required."}, status=status.HTTP_400_BAD_REQUEST)

        follower = get_object_or_404(Profile, id=follower_id)
        following = get_object_or_404(Profile, id=following_id)

        follow_instance = Follow.objects.filter(follower=follower, following=following).first()
        if not follow_instance:
            return Response({"detail": "You are not following this user."}, status=status.HTTP_400_BAD_REQUEST)

        follow_instance.delete()
        return Response({"detail": "Unfollowed successfully."}, status=status.HTTP_204_NO_CONTENT)




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
