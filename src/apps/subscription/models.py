from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import Q
from djmoney.models.fields import MoneyField
from djmoney.models.validators import MinMoneyValidator, MaxMoneyValidator

from base.services import validate_size_image, get_path_upload_subscription_image
from base.utils import get_user_class


class UserSubscriptionType(models.Model):
    owner = models.ForeignKey(get_user_class(), on_delete=models.CASCADE, related_name='subscription_types')
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

    class Meta:
        ordering = ('owner', 'price',)

    def __str__(self):
        return f"{self.name}(id: {str(self.pk)})"


class SponsorshipSubscription(models.Model):
    user = models.ForeignKey(get_user_class(), on_delete=models.CASCADE, related_name='subscriptions')
    subscription = models.ForeignKey(UserSubscriptionType, on_delete=models.CASCADE, related_name='subscribers')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'subscription'], name='unique_subscription'),
        ]

        ordering = ['-created']

    def __str__(self):
        return f"{self.user} is subscribed to {self.subscription}"
