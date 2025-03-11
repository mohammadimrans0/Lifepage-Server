from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import serializers
from .models import Profile, Follow
from django.core.exceptions import ObjectDoesNotExist
from post.serializers import PostSerializer  


class FollowerAndFollowingSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    
    class Meta:
        model = Profile
        fields = ['id', 'name', 'image']  # Only necessary fields


# Profile Serializer
class ProfileSerializer(serializers.ModelSerializer):
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()
    bookmarks = PostSerializer(many=True, read_only=True)
    image = serializers.ImageField(required=False)
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            'id', 'name', 'image', 'bio', 'status', 'contact_info',
            'followers', 'following', 'followers_count', 'following_count',
            'bookmarks', 'created_at', 'updated_at'
        ]

    def get_followers(self, obj):
        followers = Follow.objects.filter(following=obj).select_related('follower')
        follower_profiles = [follow.follower for follow in followers]
        self.context['followers_count'] = len(follower_profiles)  # Store count in context
        return FollowerAndFollowingSerializer(follower_profiles, many=True).data

    def get_following(self, obj):
        following = Follow.objects.filter(follower=obj).select_related('following')
        following_profiles = [follow.following for follow in following]
        self.context['following_count'] = len(following_profiles)  # Store count in context
        return FollowerAndFollowingSerializer(following_profiles, many=True).data

    def get_followers_count(self, obj):
        return self.context.get('followers_count', 0)

    def get_following_count(self, obj):
        return self.context.get('following_count', 0)


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        profile = instance.profile

        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.save()

        # Ensure profile data exists before updating
        if profile_data:
            profile.name = profile_data.get('name', profile.name)
            if 'image' in profile_data:  # Only update if image is provided
                profile.image = profile_data.get('image', profile.image)
            profile.bio = profile_data.get('bio', profile.bio)
            profile.status = profile_data.get('status', profile.status)
            profile.contact_info = profile_data.get('contact_info', profile.contact_info)
            profile.save()

        return instance



# Follow Serializer
class FollowSerializer(serializers.ModelSerializer):
    follower_id = serializers.IntegerField(write_only=True)
    following_id = serializers.IntegerField(write_only=True)
    created_at = serializers.DateTimeField(read_only=True)  # Include in response

    class Meta:
        model = Follow
        fields = ['follower_id', 'following_id', 'created_at']

    @transaction.atomic
    def create(self, validated_data):
        try:
            follower = Profile.objects.get(id=validated_data['follower_id'])
            following = Profile.objects.get(id=validated_data['following_id'])
        except Profile.DoesNotExist:
            raise serializers.ValidationError("One or both profiles do not exist.")

        if follower == following:
            raise serializers.ValidationError("You cannot follow yourself.")

        follow, created = Follow.objects.get_or_create(follower=follower, following=following)

        if not created:
            raise serializers.ValidationError("You are already following this user.")

        return follow




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
    

    """
    {
    "follower_id": 1,
    "following_id": 2
}
    """