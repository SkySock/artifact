from django.db import models

from apps.posts.models.post import Post


class Like(models.Model):
    user = models.ForeignKey('users.ArtifactUser', on_delete=models.CASCADE, related_name='liked_posts')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'post'], name='unique_like'),
        ]
