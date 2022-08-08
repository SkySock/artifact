from django.core.validators import FileExtensionValidator
from django.db import models

from base.services import get_path_upload_post_file, get_path_upload_post_preview
from base.validators import FileSizeValidator


class Post(models.Model):
    author = models.ForeignKey('users.ArtifactUser', on_delete=models.CASCADE, related_name="posts")
    preview = models.ImageField(
        upload_to=get_path_upload_post_preview,
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg', ]),
            FileSizeValidator(megabyte_limit=32)
        ],
    )
    views_count = models.IntegerField(default=0)
    likes_count = models.IntegerField(default=0)
    level_subscription = models.ForeignKey(
        'subscription.UserSubscriptionType',
        on_delete=models.SET_NULL,
        related_name='posts',
        null=True,
        default=None
    )
    created = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=2000, blank=True)

    class Meta:
        ordering = ('-created', )

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
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg', ]),
            FileSizeValidator(megabyte_limit=32)
        ],
    )
    queue_mark = models.IntegerField(default=-1)
