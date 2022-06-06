from django.db import models


class Post(models.Model):
    author = models.ForeignKey('users.ArtifactUser', on_delete=models.CASCADE, related_name="posts")
    views_count = models.IntegerField(default=0)
    likes_count = models.IntegerField(default=0)
    # view_level = models.Choices()
    # download_level = models.Choices()
    created = models.DateTimeField(auto_now_add=True)


class Body(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='body')
    description = models.TextField(max_length=2000, blank=True)


class MediaContent(models.Model):
    post_body = models.ForeignKey(Body, on_delete=models.CASCADE, related_name='content')
    file = models.FileField()  # TODO
    # status = models.Choices()
    queue_mark = models.IntegerField(default=-1)
