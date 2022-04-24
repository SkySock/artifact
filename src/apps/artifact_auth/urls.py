from django.urls import path
from .views import telegram_auth


urlpatterns = [
    path('telegram/', telegram_auth),
]