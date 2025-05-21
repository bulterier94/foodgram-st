from django.db import models

from recipes.models import Recipe
from users.models import User


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(
        User,
        related_name='favorite_recipe_user',
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='favorite_recipe',
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe',],
                name='favorite_recipe',
            )
        ]

        verbose_name = 'рецепт в избранном'
        verbose_name_plural = 'Рецепты в избранном'

    def __str__(self):
        username = self.user.username
        recipe = self.recipe.name
        return f'Рецепт "{recipe}" в избранном у "{username}"'
