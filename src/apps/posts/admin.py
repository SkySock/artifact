from django.contrib import admin
from src.apps.posts.models import post, comment, view, like


@admin.register(post.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author',)
    list_display_links = ('author',)


@admin.register(comment.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post',)
    list_display_links = ('post',)
