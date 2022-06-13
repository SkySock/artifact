from django.urls import path
from .endpoint import auth_views, views, following_views


urlpatterns = [
    path("", views.UserListView.as_view()),
    path('profile/<int:pk>', views.ProfileView.as_view()),
    path("follow/<int:pk>/", following_views.FollowView.as_view()),
    path("following/", following_views.UserFollowingViewSet.as_view()),
    path("followers/", following_views.UserFollowersViewSet.as_view()),
]
