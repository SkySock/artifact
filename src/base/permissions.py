from rest_framework.permissions import BasePermission, SAFE_METHODS

from src.apps.posts.models.post import Post
from src.apps.posts.services.posts import post_service
from src.apps.subscription.models import UserSubscriptionType
from src.apps.users.models import ArtifactUser, SocialLink


class IsOptions(BasePermission):
    """
    The request type is OPTIONS
    """
    def has_permission(self, request, view):
        return request.method == 'OPTIONS'


class IsPostAuthor(BasePermission):
    def has_object_permission(self, request, view, obj: Post):
        return obj.author == request.user


class IsAccessPost(BasePermission):
    def has_object_permission(self, request, view, obj: Post):
        return post_service.check_view_access(obj, request.user)


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


class IsSubscriptionTypeOwner(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj: UserSubscriptionType):
        return obj.owner == request.user
