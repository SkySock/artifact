from django.urls import path
from .views import posts, likes

urlpatterns = [
    path('', posts.CreatePostView.as_view(), name='create_post'),
    path('<int:pk>/', posts.RetrieveUpdateDestroyPostView.as_view({
        'get': 'retrieve',
        'patch': 'partial_update',
        'delete': 'destroy',
    }), name='retrieve_update_destroy_post'),
    path('<int:pk>/file/', posts.AddFileInPost.as_view(), name='add_file_post'),
    path('<int:pk>/publish/', posts.ToPublishPostView.as_view(), name='to_publish_post'),
    path('<int:pk>/like/', likes.LikeView.as_view(), name='like_post')
]
