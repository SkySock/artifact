from rest_framework.permissions import BasePermission, SAFE_METHODS

from apps.users.models import ArtifactUser, SocialLink


class IsOptions(BasePermission):
    """
    The request type is OPTIONS
    """
    def has_permission(self, request, view):
        return request.method == 'OPTIONS'


class IsProfileOwner(BasePermission):
    """
    The request of current a user, or is a read-only request
    """
    def has_object_permission(self, request, view, obj: ArtifactUser):
        return obj == request.user


class IsSocialLinkOwner(BasePermission):
    """
    The request of current a user, or is a read-only request
    """
    def has_object_permission(self, request, view, obj: SocialLink):
        return obj.user == request.user
