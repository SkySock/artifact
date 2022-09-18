from rest_framework import serializers

from src.apps.posts.models.post import Post


class IsLikeSerializer(serializers.Serializer):
    is_liked = serializers.BooleanField()


class PostStatsLikesAndViewsSerializer(serializers.ModelSerializer):
    is_liked = serializers.BooleanField(read_only=True)

    class Meta:
        model = Post
        fields = ('likes_count', 'views_count', 'is_liked', )
        read_only_fields = ('likes_count', 'views_count', )
