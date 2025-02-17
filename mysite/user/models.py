from django.db import models
from django.contrib.auth.models import User
from post.models import Post
from cloudinary.models import CloudinaryField

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=255, blank=True, null=True)
    image = CloudinaryField("image", folder="lifepage/user", default="https://res.cloudinary.com/dzuro3ezl/image/upload/v1739786072/lifepage/user/njp6vfunnf1as8g4fcqp.png")
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
    follower = models.ForeignKey(Profile, related_name='follower_id', on_delete=models.CASCADE)
    following = models.ForeignKey(Profile, related_name='following_id', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower.user.username} following {self.following.user.username}"
    


    """
    {
"follower_id" : 1,
"following_id": 2
}
    """
