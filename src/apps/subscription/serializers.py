from django.contrib.auth.models import AnonymousUser
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.subscription.models import UserSubscription, SponsorshipSubscription


class UserSubscriptionDetailSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = UserSubscription
        fields = ('id', 'owner', 'name', 'description', 'image', 'price')

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
