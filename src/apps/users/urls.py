from django.urls import path
from .endpoint import auth_views, views, following_views


urlpatterns = [
    path("", views.UserListView.as_view()),

    path('profile/<int:pk>/', views.ProfileView.as_view()),
    path('profile/avatar/', views.UpdateUserPhotoView.as_view()),

    path("follow/<int:pk>/", following_views.FollowView.as_view()),
    path("following/me/", following_views.UserFollowingViewSet.as_view()),
    path("followers/me/", following_views.UserFollowersViewSet.as_view()),
    path("following/<int:pk>/", following_views.FollowingUsersByIdViewSet.as_view()),
    path("followers/<int:pk>/", following_views.FollowersByIdViewSet.as_view()),

    path("social_links/", views.SocialLinkView.as_view({'get': 'list', 'post': 'create', })),
    path("social_links/<int:pk>", views.SocialLinkView.as_view({'put': 'update', 'delete': 'destroy', })),
]
