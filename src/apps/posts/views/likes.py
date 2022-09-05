import django
from django.db import transaction
from django.http import Http404
from drf_spectacular.utils import extend_schema
from rest_framework import views, permissions, response

from src.apps.posts.models.like import Like
from src.apps.posts.models.post import Post
from src.apps.posts.services.likes import like_service
from src.apps.posts.serializers.likes import IsLikeSerializer


class LikeView(views.APIView):
    """
    Check, like, unlike
    """
    permission_classes = (permissions.IsAuthenticated, )

    @extend_schema(
        description='Check like',
        request=None,
        responses=IsLikeSerializer,
    )
    def get(self, request, pk):
        result = like_service.is_like_exist(request.user.pk, pk)

        return response.Response({'is_liked': result})

    @extend_schema(
        description='Like',
        request=None,
        responses=IsLikeSerializer,
    )
    def post(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return response.Response({'error': 'Post does not exists'}, status=404)
        result = like_service.create_like(request.user, post)

        return response.Response({'is_liked': result}, status=201)

    @extend_schema(
        description='Unlike',
        request=None,
        responses={204: IsLikeSerializer}
    )
    def delete(self, request, pk):
        try:
            like_service.unlike(request.user.pk, pk)
        except Http404:
            return response.Response({'error': 'Like does not exists'}, status=404)

        return response.Response({'is_liked': False}, status=204)
