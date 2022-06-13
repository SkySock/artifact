import django.db
from drf_spectacular.utils import extend_schema
from rest_framework import views, generics, permissions, response
from ..models import UserFollowing, ArtifactUser
from ..serializers import UserFollowingSerializer, UserFollowersSerializer
from ..services import PaginationUsers
import base.permissions as art_permissions


class UserFollowingViewSet(generics.ListAPIView):
    """
    List of subscriptions of an authorized user
    """
    permission_classes = (permissions.IsAuthenticated | art_permissions.IsOptions,)
    serializer_class = UserFollowingSerializer
    pagination_class = PaginationUsers

    def get_queryset(self):
        return UserFollowing.objects.filter(user=self.request.user)


class UserFollowersViewSet(generics.ListAPIView):
    """
    List of subscribers of an authorized user
    """
    permission_classes = (permissions.IsAuthenticated | art_permissions.IsOptions,)
    serializer_class = UserFollowersSerializer
    pagination_class = PaginationUsers

    def get_queryset(self):
        return UserFollowing.objects.filter(following_user=self.request.user)


class FollowView(views.APIView):
    """
    Check, follow, unfollow
    """
    permission_classes = (permissions.IsAuthenticated | art_permissions.IsOptions, )

    @extend_schema(
        description='Check following',
        responses=bool,
    )
    def get(self, request, pk):
        try:
            ArtifactUser.objects.get(id=pk)
        except ArtifactUser.DoesNotExist:
            return response.Response({'error': 'User does not exist'}, status=404)

        try:
            UserFollowing.objects.get(user=request.user, following_user=pk)
        except UserFollowing.DoesNotExist:
            return response.Response(False)
        return response.Response(True)

    @extend_schema(
        description='Follow',
        responses=bool,
    )
    def post(self, request, pk):
        try:
            user = ArtifactUser.objects.get(id=pk)
            UserFollowing.objects.create(user=request.user, following_user=user)
        except ArtifactUser.DoesNotExist:
            return response.Response({'error': 'User does not exist'}, status=404)
        except django.db.IntegrityError:
            return response.Response(True, status=200)

        return response.Response(True, status=201)

    @extend_schema(
        description='Unfollow',
        responses={204: bool}
    )
    def delete(self, request, pk):
        try:
            follow = UserFollowing.objects.get(
                user=request.user,
                following_user=pk
            )
        except UserFollowing.DoesNotExist:
            return response.Response(status=404)
        follow.delete()
        return response.Response(False, status=204)
