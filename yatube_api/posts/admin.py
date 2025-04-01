from django.contrib import admin

from .models import Post, Comment, Follow


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'pub_date', 'text', 'image')
    search_fields = ('author__username', 'text')
    list_filter = ('pub_date', 'author')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'post', 'created', 'text')
    search_fields = ('author__username', 'text')
    list_filter = ('created', 'author')


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'following')
    search_fields = ('user__username', 'following__username')
    list_filter = ('user',)
