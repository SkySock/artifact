from django.http import Http404

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

    def publish(self, pk, publication_at=None):
        if publication_at:
            try:
                post = Post.objects.get(pk=pk)
            except Post.DoesNotExist:
                raise Http404
            post.publication_at = publication_at
            post.save()

            publish.apply_async(
                (pk, ),
                eta=publication_at
            )
        else:
            publish(pk)


post_service = PostService()
