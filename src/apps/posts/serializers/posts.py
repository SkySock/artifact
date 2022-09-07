from django.contrib.auth.models import AnonymousUser
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers, exceptions

from src.apps.posts.models.post import Post, MediaContent
from src.apps.posts.services.posts import post_service
from src.apps.users.models import ArtifactUser
from src.apps.users.serializers import UserBaseSerializer


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
        media_content: MediaContent = post.content.first()
        if isinstance(media_content, MediaContent):

            try:
                url = media_content.file.url
            except AttributeError:
                return ''
            request = self.context.get('request', None)
            if request is not None:
                return request.build_absolute_uri(url)
            return url
        return ''


class PostMediaContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaContent
        fields = ('id', 'file', )


class PostSerializer(serializers.ModelSerializer):
    content = PostMediaContentSerializer(many=True, read_only=True)
    author = UserBaseSerializer(read_only=True)

    class Meta:
        model = Post
        fields = (
            'id',
            'description',
            'content',
            'level_subscription',
            'author',
            'publication_at',
            'views_count',
            'likes_count',
            'status',
        )
        read_only_fields = ('views_count', 'likes_count', 'author', 'publication_at', 'status', )


class CreatePostSerializer(serializers.ModelSerializer):
    content = PostMediaContentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'description', 'content', 'level_subscription', 'publication_at', 'status', )
        read_only_fields = ('publication_at', 'status', )

    def validate_level_subscription(self, value):
        """
        Check that the request user is the owner of the subscription type.
        """
        request = self.context.get('request')
        if not request:
            return value

        if not value:
            return value

        user = request.user
        if type(user) == ArtifactUser:
            user_subs_types = user.subscription_types.all()
            if value not in user_subs_types:
                raise exceptions.ValidationError('The subscription type does not belong to the user.')

        return value
