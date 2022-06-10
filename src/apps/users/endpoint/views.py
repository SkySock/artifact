from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from ..models import ArtifactUser
from ..serializers import UserBaseSerializer
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
