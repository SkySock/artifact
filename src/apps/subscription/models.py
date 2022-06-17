from django.core.validators import FileExtensionValidator
from django.db import models
from djmoney.models.fields import MoneyField
from djmoney.models.validators import MinMoneyValidator, MaxMoneyValidator

from base.services import validate_size_image, get_path_upload_subscription_image
from base.utils import get_user_class


class UserSubscription(models.Model):
    owner = models.ForeignKey(get_user_class(), on_delete=models.CASCADE, related_name='subscriptions')
    name = models.CharField(max_length=40)
    description = models.TextField(max_length=2000)
    image = models.ImageField(
        max_length=255,
        upload_to=get_path_upload_subscription_image,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png', ]), validate_size_image]
    )
    price = MoneyField(
        max_digits=8,
        decimal_places=2,
        validators=[
            MinMoneyValidator({'RUB': 15}),
            MaxMoneyValidator({'RUB': 100_000}),
        ],
        default_currency='RUB'
    )
