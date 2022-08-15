from django.db import transaction
from drf_spectacular.utils import extend_schema
from rest_framework import generics, mixins, response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated

from apps.subscription.models import UserSubscriptionType, SponsorshipSubscription
from apps.subscription.serializers import UserSubscriptionDetailSerializer, SubscriptionSerializer
from apps.subscription.services.subs import subs_relations
from base.classes import CreateRetrieveUpdateDestroy
from base.permissions import IsSubscriptionTypeOwner
from base.serializers import MessageSerializer


class SubscriptionTypeCRUDView(CreateRetrieveUpdateDestroy):
    """
    Subscription CRUD
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    permission_classes_by_action = {
        'partial_update': [IsSubscriptionTypeOwner, ],
        'destroy': [IsSubscriptionTypeOwner, ],
    }
    serializer_class = UserSubscriptionDetailSerializer
    queryset = UserSubscriptionType.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SubscriptionView(GenericAPIView):
    permission_classes = (IsAuthenticated, )

    @extend_schema(
        description='Check subscribed',
        responses=SubscriptionSerializer,
    )
    def get(self, request, *args, **kwargs):
        try:
            UserSubscriptionType.objects.get(id=self.kwargs.get(self.lookup_field))
        except UserSubscriptionType.DoesNotExist:
            return response.Response({'error': 'Subscription type does not exist'}, status=404)

        try:
            SponsorshipSubscription.objects.get(user=request.user, subscription=self.kwargs.get(self.lookup_field))
        except SponsorshipSubscription.DoesNotExist:
            return response.Response({'is_subscribed': False})
        return response.Response({'is_subscribed': True})

    @extend_schema(
        description='Subscribe',
        responses={
            201: MessageSerializer,
            404: MessageSerializer
        },
    )
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        success, msg = subs_relations.subscribe(request.user, self.kwargs.get(self.lookup_field))
        if success:
            return response.Response({'message': msg}, status=201)
        return response.Response({'message': msg}, status=404)

    @extend_schema(
        description='Unsubscribe',
        responses={
            201: MessageSerializer,
            404: MessageSerializer
        },
    )
    def delete(self, request, *args, **kwargs):
        success, msg = subs_relations.unsubscribe(request.user, self.kwargs.get(self.lookup_field))
        if success:
            return response.Response({'message': msg}, status=201)
        return response.Response({'message': msg}, status=404)
