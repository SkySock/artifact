from rest_framework.permissions import BasePermission, SAFE_METHODS

from apps.subscription.models import UserSubscription
from apps.users.models import ArtifactUser, SocialLink


class IsOptions(BasePermission):
    """
    The request type is OPTIONS
    """
    def has_permission(self, request, view):
        return request.method == 'OPTIONS'


class IsProfileOwner(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj: ArtifactUser):
        return obj == request.user


class IsSocialLinkOwner(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj: SocialLink):
        return obj.user == request.user


class IsSubscriptionOwner(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj: UserSubscription):
        return obj.owner == request.user
