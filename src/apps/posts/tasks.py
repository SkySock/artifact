from src.apps.posts.models.post import Post
from src.config.celery import app


@app.task
def publish(pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return None

    post.publish()
