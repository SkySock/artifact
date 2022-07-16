from django.shortcuts import render
from rest_framework import generics, mixins
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly

from apps.subscription.models import UserSubscriptionType
from apps.subscription.serializers import UserSubscriptionDetailSerializer
from base.classes import CreateRetrieveUpdateDestroy
from base.permissions import IsSubscriptionOwner


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
    queryset = UserSubscriptionType.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
