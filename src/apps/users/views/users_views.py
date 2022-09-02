from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from src.apps.users.models import ArtifactUser
from ..serializers import UserBaseSerializer, ProfileSerializer, UserProfileImageSerializer, SocialLinkSerializer, \
    ProfileSettingsSerializer
from src.base.permissions import IsOptions, IsProfileOwner, IsSocialLinkOwner
from ..services import PaginationUsers
from ...subscription.serializers import UserSubscriptionDetailSerializer


class UserListView(generics.ListAPIView):
    """
    A list of users
    """
    permission_classes = (AllowAny,)
    serializer_class = UserBaseSerializer
    pagination_class = PaginationUsers
    queryset = ArtifactUser.objects.all()


class ProfileView(generics.RetrieveAPIView):
    """
    Profile
    """
    serializer_class = ProfileSerializer
    queryset = ArtifactUser.objects.all().prefetch_related('social_links')


class UpdateProfileSettings(generics.UpdateAPIView):
    """
        Update profile settings
    """
    permission_classes = (IsProfileOwner,)
    serializer_class = ProfileSettingsSerializer

    def get_object(self):
        obj = self.request.user
        self.check_object_permissions(self.request, obj)
        return obj


class UpdateUserPhotoView(generics.UpdateAPIView):
    """
    Update profile image
    """
    permission_classes = (IsProfileOwner,)
    serializer_class = UserProfileImageSerializer

    def get_object(self):
        obj = self.request.user
        self.check_object_permissions(self.request, obj)
        return obj


class SocialLinkView(viewsets.ModelViewSet):
    serializer_class = SocialLinkSerializer
    permission_classes = (IsSocialLinkOwner, IsAuthenticated, )

    def get_queryset(self):
        return self.request.user.social_links.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SubscriptionsListView(generics.ListAPIView):
    """
    A list of subscriptions
    """
    permission_classes = (AllowAny,)
    serializer_class = UserSubscriptionDetailSerializer

    def get_queryset(self):
        return ArtifactUser.objects.get(pk=self.kwargs.get(self.lookup_field)).subscription_types.all()
