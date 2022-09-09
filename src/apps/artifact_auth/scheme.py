from django.utils.translation import gettext_lazy as _
from drf_spectacular.extensions import OpenApiAuthenticationExtension
from .services.auth_backend import AuthBackend


class JWTTokenScheme(OpenApiAuthenticationExtension):
    target_class = AuthBackend
    name = 'jwtTokenAuth'

    def get_security_definition(self, auto_schema):
        return {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': _(
                'Token-based authentication with required prefix "%s"'
            ) % "Token"
        }