from rest_framework import serializers

from apps.posts.models.post import Post


class PreviewPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = (
            'id',
            'author',
            'preview_image',
            'media', 'description',
            'views_count',
            'likes_count',
            'subscription_level',
        )
