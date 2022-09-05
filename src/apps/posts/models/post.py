from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone

from src.base.services import get_path_upload_post_file
from src.base.validators import FileSizeValidator


class Post(models.Model):
    author = models.ForeignKey('users.ArtifactUser', on_delete=models.CASCADE, related_name="posts")
    views_count = models.IntegerField(default=0)
    likes_count = models.IntegerField(default=0)
    level_subscription = models.ForeignKey(
        'subscription.UserSubscriptionType',
        on_delete=models.SET_NULL,
        related_name='posts',
        null=True,
        blank=True,
        default=None
    )
    created_at = models.DateTimeField(auto_now_add=True)
    publication_at = models.DateTimeField(null=True, blank=True)
    description = models.TextField(max_length=2000, blank=True)
    is_published = models.BooleanField(default=False)

    class Meta:
        ordering = ('-publication_at', )

    def __str__(self):
        return f'Post (id: {str(self.pk)})'

    def get_unique_views_count(self):
        return self.viewed_users.count()

    def get_likes_count(self):
        return self.likes.count()

    def publish(self) -> None:
        if not self.is_published:
            self.publication_at = timezone.now()
            self.is_published = True
            self.save()

    def add_like(self):
        self.likes_count += 1
        self.save()

    def delete_like(self):
        self.likes_count -= 1
        self.save()


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
    created_at = models.DateTimeField(auto_now_add=True)
