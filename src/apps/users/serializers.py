from rest_framework import serializers
from .models import UserFollowing, ArtifactUser


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

    def get_is_followed(self, obj):
        request = self.context.get('request')
        if not request:
            return None
        try:
            UserFollowing.objects.get(user=request.user, following_user=obj)
        except UserFollowing.DoesNotExist:
            return False
        return True

    def get_followers_count(self, obj):
        return UserFollowing.objects.filter(following_user=obj).count()


class ProfileSerializer(serializers.ModelSerializer):
    """
    Profile detail serializer
    """
    avatar = serializers.ImageField(read_only=True)
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
        )


    def get_followers_count(self, obj):
        return UserFollowing.objects.filter(following_user=obj).count()

    def get_following_count(self, obj):
        return UserFollowing.objects.filter(user=obj).count()


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
