from django.contrib.auth.models import AnonymousUser
from drf_spectacular.utils import extend_schema_field, extend_schema_serializer, OpenApiExample
from rest_framework import serializers

from apps.subscription.models import UserSubscription, SponsorshipSubscription
from apps.users.models import ArtifactUser


@extend_schema_serializer(
    examples=[
         OpenApiExample(
            'Valid example 1',
            value={
                'name': "string",
                'description': "string",
                'image': "png",
                'price': "150.00",
                'price_currency': "RUB"
            },
            request_only=True,
         ),
    ]
)
class UserSubscriptionDetailSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = UserSubscription
        fields = ('id', 'owner', 'name', 'description', 'image', 'price', 'price_currency', 'is_subscribed')
        read_only_fields = ("owner",)

    @extend_schema_field(field=serializers.BooleanField())
    def get_is_subscribed(self, obj: UserSubscription):
        request = self.context.get('request')
        if not request:
            return None
        if type(request.user) == AnonymousUser:
            return False
        try:
            SponsorshipSubscription.objects.get(user=request.user, subscription=obj)
        except SponsorshipSubscription.DoesNotExist:
            return False
        return True
