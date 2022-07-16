from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('auth/', include('apps.artifact_auth.urls')),
    path('users/', include('apps.users.urls')),
    path('subscription-types/', include('apps.subscription.urls')),
]
