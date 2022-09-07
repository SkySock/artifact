from django.shortcuts import get_object_or_404
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from src.apps.posts.models.post import Post
from src.apps.posts.serializers.posts import PreviewPostSerializer
from src.apps.posts.services.posts import post_service
from src.apps.users.models import ArtifactUser


class PublishedPostsListPreviews(generics.ListAPIView):
    """
        A list of posts
    """
    permission_classes = (AllowAny,)
    serializer_class = PreviewPostSerializer

    def get_queryset(self):
        user = get_object_or_404(ArtifactUser, pk=self.kwargs.get(self.lookup_field))
        return post_service.get_published_posts_queryset_by_user(user)


class DraftPostsListPreviews(generics.ListAPIView):
    """
        A list of drafts
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = PreviewPostSerializer

    def get_queryset(self):
        user = self.request.user
        return post_service.get_draft_posts_queryset_by_user(user)


@extend_schema(
    parameters=[
        OpenApiParameter("status", OpenApiTypes.STR, OpenApiParameter.QUERY, enum=Post.Status.values),
    ]
)
class PostsListPreviews(generics.ListAPIView):
    """
        A list of posts
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = PreviewPostSerializer

    def get_queryset(self):
        user = self.request.user
        status = self.request.query_params.get('status')
        match status:
            case Post.Status.WAITING.value:
                return post_service.get_waiting_publish_posts_queryset_by_user(user)
            case Post.Status.DRAFT.value:
                return post_service.get_draft_posts_queryset_by_user(user)
            case Post.Status.PUBLISHED.value:
                return post_service.get_published_posts_queryset_by_user(user)
            case _:
                return post_service.get_published_posts_queryset_by_user(user)
