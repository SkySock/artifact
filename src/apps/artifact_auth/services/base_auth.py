from datetime import datetime, timedelta, timezone

import jwt
from django.conf import settings


def create_token(user_id: int):
    """
    Create JWT token
    """
    access_token_expires = timedelta(minutes=settings.JWT.get('ACCESS_TOKEN_EXPIRE_MINUTES', 5))
    return {
        'user_id': user_id,
        'access_token': create_access_token(
            data={'user_id': user_id},
            expires_delta=access_token_expires,
        ),
        'token_type': 'Token',
    }


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now(tz=timezone.utc) + expires_delta
    to_encode.update({'exp': expire, 'sub': 'access'})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT.get('ALGORITHM', 'HS256'))
    return encoded_jwt
