from django.urls import path
from . import views


urlpatterns = [
    path('', views.CreatePostView.as_view(), name='create_post'),
    path('<int:pk>', views.UpdatePostView.as_view(), name='update_post'),
    path('<int:pk>/file', views.AddFileInPost.as_view(), name='add_file_post'),
]
