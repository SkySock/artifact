from django.db import models


class Comment(models.Model):
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey('users.ArtifactUser', on_delete=models.CASCADE, related_name='comments')
    message = models.TextField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
