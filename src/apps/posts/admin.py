from django.contrib import admin
from apps.posts.models import post, comment


@admin.register(post.Post)
class UserFollowingAdmin(admin.ModelAdmin):
    list_display = ('id', 'author',)
    list_display_links = ('author',)


@admin.register(comment.Comment)
class UserFollowingAdmin(admin.ModelAdmin):
    list_display = ('id', 'post',)
    list_display_links = ('post',)
