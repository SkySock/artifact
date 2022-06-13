from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from ..models import ArtifactUser
from ..serializers import UserBaseSerializer, ProfileSerializer
from base.permissions import IsOptions
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
    serializer_class = ProfileSerializer
    queryset = ArtifactUser.objects.all()

