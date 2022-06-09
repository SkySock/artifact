from django.urls import path
from .views import telegram_auth, CheckAuthMe

urlpatterns = [
    path('telegram/', telegram_auth),
    path('me/', CheckAuthMe.as_view()),
]