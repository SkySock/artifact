from django.urls import path
from .views import posts


urlpatterns = [
    path('', posts.CreatePostView.as_view(), name='create_post'),
    path('<int:pk>', posts.UpdatePostView.as_view(), name='update_post'),
    path('<int:pk>/file', posts.AddFileInPost.as_view(), name='add_file_post'),
    path('<int:pk>/publish', posts.ToPublishPostView.as_view(), name='to_publish_post'),
]
