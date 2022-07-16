from django.urls import path
from . import views


urlpatterns = [
    path("", views.SubscriptionView.as_view({
        'post': 'create',
    })),
    path("<int:pk>/", views.SubscriptionView.as_view({
        'get': 'retrieve',
        'patch': 'update',
        'delete': 'destroy',
    })),
]
