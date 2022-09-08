from django.http import HttpResponseNotModified, Http404
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import generics, status, viewsets, serializers, mixins
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from src.apps.users.serializers import PublicationAtSerializer
from src.apps.posts.services.posts import post_service
from src.apps.posts.models.post import Post, MediaContent
from src.apps.posts.serializers.posts import PostSerializer, PostMediaContentSerializer, CreatePostSerializer
from src.base.classes import ActionPermissionMixin, ActionSerializerMixin
from src.base.exceptions import PostNotModified
from src.base.permissions import IsPostAuthor, IsAccessPost, IsPostFileOwner


class CreatePostView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = CreatePostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class RetrieveUpdateDestroyPostView(mixins.RetrieveModelMixin,
                                    mixins.UpdateModelMixin,
                                    mixins.DestroyModelMixin,
                                    ActionPermissionMixin,
                                    ActionSerializerMixin,
                                    viewsets.GenericViewSet):

    permission_classes = (IsAuthenticated, IsPostAuthor, )
    permission_classes_by_action = {
        'retrieve': (IsAuthenticated, IsAccessPost, ),
    }
    serializer_class = CreatePostSerializer
    serializer_class_by_action = {
        'partial_update': CreatePostSerializer,
        'retrieve': PostSerializer,
    }
    queryset = Post.objects.all().prefetch_related('content')

    def retrieve(self, request, *args, **kwargs):
        instance: Post = self.get_object()
        post_service.add_view(self.request.user, instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


@extend_schema(
        request=PostMediaContentSerializer,
        responses={201: CreatePostSerializer},
    )
class AddFileInPost(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, IsPostAuthor, )
    serializer_class = PostMediaContentSerializer

    def get_post_object(self):
        posts = Post.objects.all()
        obj = generics.get_object_or_404(posts, pk=self.kwargs.get(self.lookup_field))
        self.check_object_permissions(self.request, obj)

        return obj

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        post = self.get_post_object()
        if post.status == Post.Status.PUBLISHED:
            raise PostNotModified

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        serializer_post = CreatePostSerializer(post, context=self.get_serializer_context())

        return Response(serializer_post.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer, **kwargs):
        post = self.get_post_object()
        serializer.save(post=post)


class DeleteFilePost(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated, IsPostFileOwner,)
    serializer_class = PostMediaContentSerializer

    def get_queryset(self):
        return MediaContent.objects.filter(post=self.kwargs.get('pk'))

    def get_object(self):
        files = self.get_queryset()
        obj = generics.get_object_or_404(files, pk=self.kwargs.get('file_id'))
        self.check_object_permissions(self.request, obj)

        return obj

    def perform_destroy(self, instance: MediaContent):
        if instance.post.status == Post.Status.PUBLISHED:
            raise PostNotModified
        super().perform_destroy(instance)


@extend_schema(
        request=PublicationAtSerializer,
        responses={201: PublicationAtSerializer},
    )
class ToPublishPostView(APIView):
    permission_classes = (IsAuthenticated, IsPostAuthor)

    def post(self, request, pk):
        post = self.get_object()

        serializer = PublicationAtSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        post_service.publish(post.pk, serializer.data.get('publication_at'))

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_object(self):
        try:
            post = Post.objects.prefetch_related('content').get(pk=self.kwargs.get('pk'))
        except Post.DoesNotExist:
            raise Http404

        self.check_object_permissions(self.request, post)

        return post
