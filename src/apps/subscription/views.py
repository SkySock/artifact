from django.shortcuts import render
from rest_framework import generics, mixins
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly

from apps.subscription.models import UserSubscription
from apps.subscription.serializers import UserSubscriptionDetailSerializer
from base.classes import CreateRetrieveUpdateDestroy
from base.permissions import IsSubscriptionOwner


class SubscriptionsListView(generics.ListAPIView):
    """
    A list of subscriptions
    """
    permission_classes = (AllowAny,)
    serializer_class = UserSubscriptionDetailSerializer

    def get_queryset(self):
        return UserSubscription.objects.filter(owner=self.kwargs.get(self.lookup_field))


class SubscriptionView(CreateRetrieveUpdateDestroy):
    """
    Subscription CRUD
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    permission_classes_by_action = {
        'update': [IsSubscriptionOwner, ],
        'destroy': [IsSubscriptionOwner, ],
    }
    serializer_class = UserSubscriptionDetailSerializer
    queryset = UserSubscription.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
