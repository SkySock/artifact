from apps.posts.models.post import Post
from apps.subscription.models import UserSubscriptionType
from apps.subscription.services.subs import subs_relations
from apps.users.models import ArtifactUser


class PostService:
    def check_view_access(self, post: Post, user: ArtifactUser) -> bool:
        if post.author == user:
            return True

        if not post.level_subscription:
            return True

        access_subscription: UserSubscriptionType = post.level_subscription

        user_subscription = subs_relations.get_subscription_on_user(user, post.author)

        if not user_subscription:
            return False

        if user_subscription == access_subscription or user_subscription.price > access_subscription.price:
            return True

        return False


post_service = PostService()
