from datetime import datetime, timedelta, timezone

import jwt
from django.conf import settings
from drf_spectacular.authentication import TokenScheme
from drf_spectacular.plumbing import build_bearer_security_scheme_object


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
    }


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now(tz=timezone.utc) + expires_delta
    to_encode.update({'exp': expire, 'sub': 'access'})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT.get('ALGORITHM', 'HS256'))
    return encoded_jwt


class JWTTokenScheme(TokenScheme):
    target_class = 'apps.artifact_auth.services.auth_backend.AuthBackend'
    name = 'tokenAuth'
    match_subclasses = True
    priority = -1

    def get_security_definition(self, auto_schema):
        return build_bearer_security_scheme_object(
            header_name='Authorization',
            token_prefix='Token',
        )
