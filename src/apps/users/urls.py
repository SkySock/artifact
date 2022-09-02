from django.urls import path
from src.apps.users.views import users_views, following_views, posts_views

urlpatterns = [
    path("", users_views.UserListView.as_view()),

    path('profile/<int:pk>/', users_views.ProfileView.as_view()),
    path('profile/avatar/', users_views.UpdateUserPhotoView.as_view()),

    path('me/profile-settings/', users_views.UpdateProfileSettings.as_view()),

    path("follow/<int:pk>/", following_views.FollowView.as_view()),
    path("following/me/", following_views.UserFollowingViewSet.as_view()),
    path("followers/me/", following_views.UserFollowersViewSet.as_view()),
    path("following/<int:pk>/", following_views.FollowingUsersByIdViewSet.as_view()),
    path("followers/<int:pk>/", following_views.FollowersByIdViewSet.as_view()),

    path("<int:pk>/subscription-types/", users_views.SubscriptionsListView.as_view()),
    path("<int:pk>/posts/", posts_views.PostsListPreviews.as_view()),

    path("social-links/", users_views.SocialLinkView.as_view({'get': 'list', 'post': 'create', })),
    path("social-links/<int:pk>", users_views.SocialLinkView.as_view({'put': 'update', 'delete': 'destroy', })),
]
