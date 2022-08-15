from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.posts.models.post import Post
from apps.posts.serializers.posts import PostSerializer
from base.permissions import IsPostAuthor


class CreatePostView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UpdatePostView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated, IsPostAuthor, )
    serializer_class = PostSerializer
    queryset = Post.objects.all()
