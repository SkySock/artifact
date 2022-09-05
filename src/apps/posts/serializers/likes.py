from rest_framework import serializers


class IsLikeSerializer(serializers.Serializer):
    is_liked = serializers.BooleanField()
