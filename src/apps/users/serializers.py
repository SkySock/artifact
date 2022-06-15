from abc import ABC

from django.contrib.auth.models import AnonymousUser
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from .models import UserFollowing, ArtifactUser, SocialLink


class UserBaseSerializer(serializers.ModelSerializer):
    """
    User base detail serializer
    """
    avatar = serializers.ImageField(read_only=True)
    is_followed = serializers.SerializerMethodField('get_is_followed')
    followers_count = serializers.SerializerMethodField()

    class Meta:
        model = ArtifactUser
        fields = ('id', 'username', 'display_name', 'followers_count', 'avatar', 'is_followed')

    @extend_schema_field(field=serializers.BooleanField())
    def get_is_followed(self, obj: ArtifactUser):
        request = self.context.get('request')
        if not request:
            return None
        if type(request.user) == AnonymousUser:
            return False
        try:
            UserFollowing.objects.get(user=request.user, following_user=obj)
        except UserFollowing.DoesNotExist:
            return False
        return True

    @extend_schema_field(field=serializers.IntegerField())
    def get_followers_count(self, obj: ArtifactUser):
        return UserFollowing.objects.filter(following_user=obj).count()


class SocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLink
        fields = ('id', 'link',)


class ProfileSerializer(serializers.ModelSerializer):
    """
    Profile detail serializer
    """
    avatar = serializers.ImageField(read_only=True)
    social_links = SocialLinkSerializer(read_only=True, many=True)
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = ArtifactUser
        fields = (
            'id',
            'username',
            'display_name',
            'bio',
            'followers_count',
            'following_count',
            'avatar',
            'social_links',
        )

    @extend_schema_field(field=serializers.IntegerField())
    def get_followers_count(self, obj):
        return UserFollowing.objects.filter(following_user=obj).count()

    @extend_schema_field(field=serializers.IntegerField())
    def get_following_count(self, obj):
        return UserFollowing.objects.filter(user=obj).count()


class UserProfileImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArtifactUser
        fields = ('avatar',)


class FollowSerializer(serializers.Serializer):
    is_followed = serializers.BooleanField()


class UserFollowingSerializer(serializers.ModelSerializer):
    following_user = UserBaseSerializer(read_only=True)

    class Meta:
        model = UserFollowing
        fields = ('id', 'following_user', 'created')


class UserFollowersSerializer(serializers.ModelSerializer):
    user = UserBaseSerializer(read_only=True)

    class Meta:
        model = UserFollowing
        fields = ('id', 'user', 'created')
