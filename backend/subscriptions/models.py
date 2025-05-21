from django.db import models
from users.models import User


class Subscription(models.Model):
    subscriber = models.ForeignKey(
        User,
        related_name='subscriber',
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
    )
    subscribed_on = models.ForeignKey(
        User,
        related_name='subscribed_on',
        on_delete=models.CASCADE,
        verbose_name='Подписан на',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['subscriber', 'subscribed_on',],
                name='subscription',
            )
        ]

        verbose_name = 'подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        subscriber = self.subscriber.username
        subscribed_on = self.subscribed_on.username
        return f'"{subscriber}" подписан на "{subscribed_on}"'
