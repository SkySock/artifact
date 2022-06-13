from rest_framework import serializers
from apps.users.models import ArtifactUser


class TelegramAuthSerializer(serializers.Serializer):
    """
    Сериализация данных от Telegram
    """
    username = serializers.CharField(required=False)
    id = serializers.IntegerField()
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    hash = serializers.CharField()
    auth_date = serializers.IntegerField()
    photo_url = serializers.URLField(required=False)


class TelegramAuthResponseSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    access_token = serializers.CharField()


class UserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArtifactUser
        fields = (
            'id',
            'username',
            'display_name',
            'avatar',
        )
