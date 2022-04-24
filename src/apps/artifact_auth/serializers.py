from rest_framework import serializers


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
