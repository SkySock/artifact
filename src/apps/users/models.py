from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin

from .validators import ArtUnicodeUsernameValidator


class ArtUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not username:
            raise ValueError('The given username must be set')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


class ArtifactUser(AbstractBaseUser):
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
    join_date = models.DateTimeField(auto_now_add=True)
    bio = models.TextField(max_length=2000, blank=True)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"

    objects = ArtUserManager()

    @property
    def is_authenticated(self):
        return True

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def __str__(self):
        return str(self.pk)


class SocialLink(models.Model):
    user = models.ForeignKey(ArtifactUser, on_delete=models.CASCADE, related_name='social_links')
    link = models.URLField(max_length=100)
