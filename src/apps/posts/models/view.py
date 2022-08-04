from django.db import models
from .post import Post


class PostView(models.Model):
    user = models.ForeignKey('users.ArtifactUser', on_delete=models.CASCADE, related_name='viewed_posts')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='viewed_users')
    count = models.IntegerField()
    first_view = models.DateTimeField(auto_now_add=True)
    last_view = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'post'], name='unique_post_view'),
        ]
