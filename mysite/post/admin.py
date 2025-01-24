from django.contrib import admin
from .models import Post, LikePost, CommentPost, BookMark

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'caption', 'created_at', 'no_of_likes')
    search_fields = ('user__username', 'caption')
    list_filter = ('created_at',)

@admin.register(LikePost)
class LikePostAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'created_at')
    search_fields = ('post__id', 'user__username')

@admin.register(CommentPost)
class CommentPostAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'comment', 'created_at')
    search_fields = ('post__id', 'user__username', 'comment')

@admin.register(BookMark)
class BookMarkAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'created_at')
    search_fields = ('post__id', 'user__username')
