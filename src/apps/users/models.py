from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin

from src.base.services import get_path_upload_profile_image, get_default_profile_image, validate_size_image
from src.base.validators import FileSizeValidator
from .validators import ArtUnicodeUsernameValidator


class ArtifactUser(models.Model):
    username_validator = ArtUnicodeUsernameValidator()

    telegram_id = models.BigIntegerField(unique=True, null=True, blank=True)
    username = models.CharField(
        max_length=60,
        unique=True,
        help_text=_(
            "Required. 60 characters or fewer. Letters, digits and _ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    display_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(max_length=150, unique=True, null=True, blank=True)
    bio = models.TextField(max_length=2000, blank=True)
    avatar = models.ImageField(
        max_length=255,
        upload_to=get_path_upload_profile_image,
        blank=True,
        default='posts/defaults/default_profile_image.png',
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg', ]),
            FileSizeValidator(megabyte_limit=5)
        ]
    )
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"

    class Meta:
        ordering = ('username', )

    @property
    def is_authenticated(self):
        return True

    def __str__(self):
        return f"User {self.username}(id: {str(self.pk)})"


class SocialLink(models.Model):
    user = models.ForeignKey(ArtifactUser, on_delete=models.CASCADE, related_name='social_links')
    link = models.URLField(max_length=100)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'link'], name='unique_links', ),
        ]

        ordering = ['user']


class UserFollowing(models.Model):
    user = models.ForeignKey(
        ArtifactUser, on_delete=models.CASCADE, related_name='following'
    )
    following_user = models.ForeignKey(
        ArtifactUser, on_delete=models.CASCADE, related_name='followers'
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'following_user'], name='unique_followers',),
        ]

        ordering = ['-created']

    def __str__(self):
        return f"{self.user} follows {self.following_user}"
