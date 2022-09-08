from django.contrib import admin
from django.urls import path, include
from src.apps.posts.views.posts import DeleteFilePost

urlpatterns = [
    path('auth/', include('src.apps.artifact_auth.urls')),
    path('users/', include('src.apps.users.urls')),
    path('subscription-types/', include('src.apps.subscription.urls')),
    path('posts/', include('src.apps.posts.urls')),
]
