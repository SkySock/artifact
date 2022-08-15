from django.contrib.auth.models import AnonymousUser
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers, exceptions

from apps.posts.models.post import Post, MediaContent
from apps.posts.services.posts import post_service
from apps.users.models import ArtifactUser
from apps.users.serializers import UserBaseSerializer


class PreviewPostSerializer(serializers.ModelSerializer):
    author = UserBaseSerializer(read_only=True)
    access = serializers.SerializerMethodField()
    preview = serializers.SerializerMethodField()

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
        read_only_fields = ['author', 'views_count', 'likes_count', 'level_subscription', ]

    @extend_schema_field(field=serializers.BooleanField())
    def get_access(self, post: Post) -> bool:
        request = self.context.get('request')
        if not request:
            return False
        if type(request.user) == AnonymousUser:
            return False

        user: ArtifactUser = request.user

        return post_service.check_view_access(post=post, user=user)

    @extend_schema_field(field=serializers.ImageField())
    def get_preview(self, post: Post):
        return post.content.first()


class PostMediaContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaContent
        fields = '__all__'
        read_only_fields = ['post', ]


class PostSerializer(serializers.ModelSerializer):
    content = PostMediaContentSerializer(many=True, read_only=True)
    author = UserBaseSerializer(read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['views_count', 'likes_count', 'author', 'is_published', 'publication_at', ]

    def validate_level_subscription(self, value):
        request = self.context.get('request')
        if not request:
            return value

        user = request.user
        if type(user) == ArtifactUser:
            user_subs_types = user.subscription_types.all()
            if value not in user_subs_types:
                raise exceptions.ValidationError('sss')

        return value
