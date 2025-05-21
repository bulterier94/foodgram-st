from django.db import models

from users.models import User
from recipes.models import Recipe


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        related_name='shopping_cart_user',
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='shopping_cart_recipe',
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'user',
                    'recipe',
                ],
                name='shopping_cart',
            )
        ]

        verbose_name = 'список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self):
        username = self.user.username
        recipe = self.recipe.name
        return f'Рецепт "{recipe}" в списке покупок у "{username}"'
