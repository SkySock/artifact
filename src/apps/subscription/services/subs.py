from django.db import IntegrityError
from typing import Optional

from src.apps.subscription.models import UserSubscriptionType, SponsorshipSubscription
from src.apps.users.models import ArtifactUser


class SubscriptionRelationsService:
    def subscribe(self, user: ArtifactUser, subscription_pk: int) -> (bool, str):
        try:
            subscription_type = UserSubscriptionType.objects.get(pk=subscription_pk)
        except UserSubscriptionType.DoesNotExist:
            return False, 'SubscriptionType does not exist'

        current_subscription: SponsorshipSubscription = self.get_subscription_on_user(user, subscription_type.owner)
        if current_subscription:
            current_subscription.delete()

        try:
            SponsorshipSubscription.objects.create(user=user, subscription=subscription_type)
        except IntegrityError:
            return False, 'User already subscribed'

        return True, 'User success subscribed'


    def unsubscribe(self, user: ArtifactUser, subscription_pk: int) -> (bool, str):
        try:
            subscription = SponsorshipSubscription.objects.get(
                user=user,
                subscription=subscription_pk
            )
        except SponsorshipSubscription.DoesNotExist:
            return False, 'The user has not been subscribed'
        subscription.delete()
        return True, 'User unsubscribed'


    def get_subscription_on_user(self, subscriber: ArtifactUser, subscription_owner: ArtifactUser) -> Optional[SponsorshipSubscription]:
        try:
            sudscription = subscriber.subscriptions.get(subscription__owner=subscription_owner)
        except SponsorshipSubscription.DoesNotExist:
            return None
        return sudscription


subs_relations = SubscriptionRelationsService()
