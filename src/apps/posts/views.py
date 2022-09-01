from django.http import HttpResponseNotModified
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from src.apps.posts.models.post import Post
from src.apps.posts.serializers.posts import PostSerializer, PostMediaContentSerializer
from src.base.permissions import IsPostAuthor


class CreatePostView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UpdatePostView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated, IsPostAuthor, )
    serializer_class = PostSerializer
    queryset = Post.objects.all()


@extend_schema(
        request=PostMediaContentSerializer,
        responses={201: PostSerializer},
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
        if post.is_published:
            raise HttpResponseNotModified

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        serializer_post = PostSerializer(post)

        return Response(serializer_post.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer, **kwargs):
        post = self.get_post_object()
        serializer.save(post=post)
