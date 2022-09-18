import django
from django.db import transaction
from django.db.models import Exists, OuterRef
from django.http import Http404
from drf_spectacular.utils import extend_schema
from rest_framework import views, permissions, response, generics

from src.apps.posts.models.like import Like
from src.apps.posts.models.post import Post
from src.apps.posts.services.likes import like_service
from src.apps.posts.serializers.likes import IsLikeSerializer, PostStatsLikesAndViewsSerializer
from src.apps.users.models import ArtifactUser


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
        responses=PostStatsLikesAndViewsSerializer,
    )
    def post(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return response.Response({'error': 'Post does not exists'}, status=404)
        result = like_service.create_like(request.user, post)

        post = self.get_post_object(request, pk)
        serializer = PostStatsLikesAndViewsSerializer(post)

        return response.Response(serializer.data, status=201)

    @extend_schema(
        description='Unlike',
        request=None,
        responses={200: PostStatsLikesAndViewsSerializer}
    )
    def delete(self, request, pk):
        try:
            like_service.unlike(request.user.pk, pk)
        except Http404:
            return response.Response({'error': 'Like does not exists'}, status=404)

        post = self.get_post_object(request, pk)
        serializer = PostStatsLikesAndViewsSerializer(post)

        return response.Response(serializer.data, status=200)

    def get_post_object(self, request, pk):
        this_user: ArtifactUser = request.user
        posts = Post.objects.annotate(
            is_liked=Exists(this_user.liked_posts.filter(post=OuterRef('id')))
        )
        obj = generics.get_object_or_404(posts, pk=self.kwargs.get('pk'))
        self.check_object_permissions(request, obj)

        return obj
