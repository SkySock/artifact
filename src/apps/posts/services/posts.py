import datetime

from django.db import transaction
from django.http import Http404
from django.utils import timezone

from src.apps.posts.models.view import PostView
from src.apps.posts.tasks import publish
from src.apps.posts.models.post import Post
from src.apps.subscription.models import UserSubscriptionType
from src.apps.subscription.services.subs import subs_relations
from src.apps.users.models import ArtifactUser


class PostService:
    def check_view_access(self, post: Post, user: ArtifactUser) -> bool:
        if post.author == user:
            return True

        if not post.level_subscription:
            return True

        access_subscription: UserSubscriptionType = post.level_subscription

        user_subscription = subs_relations.get_subscription_on_user(user, post.author).subscription

        if not user_subscription:
            return False

        if user_subscription == access_subscription or user_subscription.price > access_subscription.price:
            return True

        return False

    @transaction.atomic
    def add_view(self, user: ArtifactUser, post: Post):
        try:
            view: PostView = PostView.objects.get(user=user, post=post)
        except PostView.DoesNotExist:
            view: PostView = PostView.objects.create(user=user, post=post)
            post.add_view()

        if view.last_view <= timezone.now() - datetime.timedelta(minutes=15):
            post.add_view()
            view.count += 1
            view.save()

    def publish(self, pk, publication_at=None):
        if publication_at:
            try:
                post = Post.objects.get(pk=pk)
            except Post.DoesNotExist:
                raise Http404

            if post.status == Post.Status.DRAFT:
                post.publication_at = publication_at

                publish.apply_async(
                    (pk, ),
                    eta=publication_at
                )
                post.status = Post.Status.WAITING
                post.save()
        else:
            publish(pk)

    def get_published_posts_queryset_by_user(self, user: ArtifactUser):
        return Post.objects.select_related('author').filter(
            author=user,
            status=Post.Status.PUBLISHED,
        )

    def get_draft_posts_queryset_by_user(self, user: ArtifactUser):
        return Post.objects.select_related('author')\
            .filter(author=user, status=Post.Status.DRAFT)\
            .order_by('-created_at')

    def get_waiting_publish_posts_queryset_by_user(self, user: ArtifactUser):
        return Post.objects.select_related('author')\
            .filter(author=user, status=Post.Status.WAITING)\
            .order_by('-publication_at')


post_service = PostService()
