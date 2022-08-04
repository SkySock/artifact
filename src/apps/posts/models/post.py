from django.core.validators import FileExtensionValidator
from django.db import models

from apps.posts.validators import validate_size_file
from base.services import get_path_upload_post_file


class Post(models.Model):
    author = models.ForeignKey('users.ArtifactUser', on_delete=models.CASCADE, related_name="posts")
    views_count = models.IntegerField(default=0)
    likes_count = models.IntegerField(default=0)
    view_level = models.ForeignKey(
        'subscription.UserSubscriptionType',
        on_delete=models.SET_NULL,
        related_name='posts',
        null=True
    )
    created = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=2000, blank=True)

    def __str__(self):
        return f'Post (id: {str(self.pk)})'

    def get_unique_views_count(self):
        return self.viewed_users.count()

    def get_likes_count(self):
        return self.likes.count()


class MediaContent(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='content')
    file = models.FileField(
        upload_to=get_path_upload_post_file,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg', ]), validate_size_file],
    )
    queue_mark = models.IntegerField(default=-1)
