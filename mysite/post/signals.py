from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import LikePost, CommentPost, Post

# Signal to increment no_of_likes when a LikePost is created
@receiver(post_save, sender=LikePost)
def increment_likes(sender, instance, created, **kwargs):
    if created:
        post = instance.post
        post.no_of_likes += 1
        post.save()

# Signal to decrement no_of_likes when a LikePost is deleted
@receiver(post_delete, sender=LikePost)
def decrement_likes(sender, instance, **kwargs):
    post = instance.post
    post.no_of_likes -= 1
    post.save()

# Signal to increment no_of_comments when a CommentPost is created
@receiver(post_save, sender=CommentPost)
def increment_comments(sender, instance, created, **kwargs):
    if created:
        post = instance.post
        post.no_of_comments += 1
        post.save()

# Signal to decrement no_of_comments when a CommentPost is deleted
@receiver(post_delete, sender=CommentPost)
def decrement_comments(sender, instance, **kwargs):
    post = instance.post
    post.no_of_comments -= 1
    post.save()
