from django.urls import path
from . import views


urlpatterns = [
    path("", views.SubscriptionTypeCRUDView.as_view({
        'post': 'create',
    })),
    path("<int:pk>/", views.SubscriptionTypeCRUDView.as_view({
        'get': 'retrieve',
        'patch': 'partial_update',
        'delete': 'destroy',
    })),
    path("<int:pk>/subscribe", views.SubscriptionView.as_view()),
]
