from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile, Follow
from django.core.exceptions import ObjectDoesNotExist
from post.serializers import PostSerializer

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']  

# Profile Serializer
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Serialize User data
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    followers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    following = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    bookmarks = PostSerializer(many=True, read_only=True) 

    class Meta:
        model = Profile
        fields = [
            'user', 'name', 'image', 'bio', 'status', 'contact_info',
            'followers', 'following', 'bookmarks',
            'followers_count', 'following_count',
            'created_at', 'updated_at',
        ]

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()

# Follow Serializer
class FollowSerializer(serializers.ModelSerializer):
    follower = ProfileSerializer(read_only=True)
    following = ProfileSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ['follower', 'following', 'created_at']

# Signup Serializer
class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']

    def validate(self, data):
        # Ensure passwords match
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        
        # Check for unique username and email
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({"username": "Username already exists."})
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "Email is already registered."})
        return data

    def create(self, validated_data):
        # Remove confirm_password before creating the user
        validated_data.pop('confirm_password')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required = True)
    password = serializers.CharField(required = True)


class ResetPasswordSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, write_only=True, min_length=8)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')

        # Check if user exists
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            raise serializers.ValidationError({"username": "User does not exist."})

        # Check if passwords match
        if new_password != confirm_password:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})

        return attrs

    def save(self, **kwargs):
        username = self.validated_data['username']
        new_password = self.validated_data['new_password']

        user = User.objects.get(username=username)
        user.set_password(new_password)
        user.save()

        return user