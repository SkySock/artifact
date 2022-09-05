import django
from django.db import transaction
from django.http import Http404

from src.apps.posts.models.like import Like
from src.apps.posts.models.post import Post
from src.apps.users.models import ArtifactUser


class LikeService:
    def is_like_exist(self, user_pk, post_pk) -> bool:
        try:
            Like.objects.get(user=user_pk, post=post_pk)
        except Like.DoesNotExist:
            return False
        return True

    @transaction.atomic
    def create_like(self, user: ArtifactUser, post: Post) -> bool:
        try:
            Like.objects.create(user=user, post=post)
        except django.db.IntegrityError:
            return True
        post.add_like()
        return True

    @transaction.atomic
    def unlike(self, user_pk, post_pk):
        try:
            like = Like.objects.get(
                user=user_pk,
                post=post_pk
            )
        except Like.DoesNotExist:
            raise Http404
        like.post.delete_like()
        like.delete()


like_service = LikeService()
