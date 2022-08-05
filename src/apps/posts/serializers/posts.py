from django.contrib.auth.models import AnonymousUser
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.posts.models.post import Post
from apps.posts.services.posts import post_service
from apps.users.models import ArtifactUser
from apps.users.serializers import UserBaseSerializer


class PreviewPostSerializer(serializers.ModelSerializer):

    author = UserBaseSerializer(read_only=True)
    access = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            'author',
            'preview',
            'views_count',
            'likes_count',
            'level_subscription',
            'access',
        ]
        read_only_fields = ['views_count', 'likes_count', ]

    @extend_schema_field(field=serializers.BooleanField())
    def get_access(self, post: Post) -> bool:
        request = self.context.get('request')
        if not request:
            return False
        if type(request.user) == AnonymousUser:
            return False

        user: ArtifactUser = request.user

        return post_service.check_view_access(post=post, user=user)
