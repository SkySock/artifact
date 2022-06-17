import uuid

from apps.users.models import ArtifactUser


def generate_unique_username(username: str = None):
    if not username:
        return 'artist_' + uuid.uuid4().hex.upper()

    if not ArtifactUser.objects.filter(username=username).exists():
        return username
    else:
        return username + uuid.uuid4().hex.upper()


def get_user_class():
    return ArtifactUser
