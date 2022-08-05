from django.urls import path
from .endpoint import auth_views, views, following_views, posts_views

urlpatterns = [
    path("", views.UserListView.as_view()),

    path('profile/<int:pk>/', views.ProfileView.as_view()),
    path('profile/avatar/', views.UpdateUserPhotoView.as_view()),

    path('me/profile-settings/', views.UpdateProfileSettings.as_view()),

    path("follow/<int:pk>/", following_views.FollowView.as_view()),
    path("following/me/", following_views.UserFollowingViewSet.as_view()),
    path("followers/me/", following_views.UserFollowersViewSet.as_view()),
    path("following/<int:pk>/", following_views.FollowingUsersByIdViewSet.as_view()),
    path("followers/<int:pk>/", following_views.FollowersByIdViewSet.as_view()),

    path("<int:pk>/subscription-types/", views.SubscriptionsListView.as_view()),
    path("<int:pk>/posts/", posts_views.PostsListPreviews.as_view()),

    path("social-links/", views.SocialLinkView.as_view({'get': 'list', 'post': 'create', })),
    path("social-links/<int:pk>", views.SocialLinkView.as_view({'put': 'update', 'delete': 'destroy', })),
]
