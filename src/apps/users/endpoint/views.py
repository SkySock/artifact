from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from ..models import ArtifactUser
from ..serializers import UserBaseSerializer, ProfileSerializer, UserProfileImageSerializer
from base.permissions import IsOptions, IsProfileOwner
from ..services import PaginationUsers


class UserListView(generics.ListAPIView):
    """
    A list of users
    """
    permission_classes = (IsAuthenticated | IsOptions,)
    serializer_class = UserBaseSerializer
    pagination_class = PaginationUsers
    queryset = ArtifactUser.objects.all()


class ProfileView(generics.RetrieveAPIView):
    """
    Profile
    """
    serializer_class = ProfileSerializer
    queryset = ArtifactUser.objects.all()


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
