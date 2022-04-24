import hashlib
import hmac
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed

from .. import serializers
from . import base_auth
from apps.users.models import ArtifactUser
from base.utils import generate_unique_username


def check_telegram_auth(telegram_user: serializers.TelegramAuthSerializer):
    token_bot = settings.TELEGRAM_AUTH.get('BOT_TOKEN')
    secret_key = hashlib.sha256(token_bot.encode()).digest()
    data: dict = telegram_user.data

    data.pop('hash')
    sorted_items = sorted(data.items())

    pre_check = ['='.join(map(lambda x: str(x), item)) for item in sorted_items]
    data_check_string = '\n'.join(pre_check)

    msg = bytearray(data_check_string, 'utf-8')
    processed_hash = hmac.new(secret_key, msg=msg, digestmod=hashlib.sha256).hexdigest()

    if processed_hash == telegram_user.data['hash']:
        user, _ = ArtifactUser.objects.get_or_create(
            telegram_id=telegram_user.data['id'],
            defaults={
                'display_name': f'{telegram_user.data["first_name"]} {telegram_user.data["last_name"]}',
                'username': generate_unique_username(telegram_user.data["username"]),
                'password': ArtifactUser.objects.make_random_password(length=16)
            },
        )
        return base_auth.create_token(user.pk)
    else:
        raise AuthenticationFailed(code=403, detail='Bad data telegram')
