from rest_framework import generics
from rest_framework.permissions import AllowAny

from src.apps.posts.models.post import Post
from src.apps.posts.serializers.posts import PreviewPostSerializer


class PostsListPreviews(generics.ListAPIView):
    """
        A list of posts
    """
    permission_classes = (AllowAny,)
    serializer_class = PreviewPostSerializer

    def get_queryset(self):
        return Post.objects.select_related('author').filter(
            author=self.kwargs.get(self.lookup_field),
            is_published=True
        )
