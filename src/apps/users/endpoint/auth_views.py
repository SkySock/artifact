from django.shortcuts import render


def telegram_login(request):
    return render(request, 'users/telegram_login.html')
