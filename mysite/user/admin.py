from django.contrib import admin
from .models import Profile, Follow

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'status', 'created_at', 'updated_at']
    search_fields = ['user__username', 'status', 'bio']
    list_filter = ['created_at', 'updated_at']

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['follower', 'following', 'created_at']
    search_fields = ['follower__username', 'following__username']
    list_filter = ['created_at']
