from django.db import models
from django.contrib.auth.models import User
from post.models import Post

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(
        upload_to='upload/user/images/', 
        default='upload/user/images/avatar.png'
    )
    bio = models.TextField(blank=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    contact_info = models.CharField(max_length=255, blank=True, null=True)
    followers = models.ManyToManyField(
        'self', 
        blank=True, 
        through='Follow', 
        through_fields=('following', 'follower')
    )
    following = models.ManyToManyField(
        'self',
        blank=True, 
        through='Follow', 
        through_fields=('follower', 'following')
    )
    bookmarks = models.ManyToManyField(Post, related_name='bookmarked_by_profiles', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Follow(models.Model):
    follower = models.ForeignKey(Profile, related_name='following_set', on_delete=models.CASCADE)
    following = models.ForeignKey(Profile, related_name='followers_set', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower.user.username} following {self.following.user.username}"
