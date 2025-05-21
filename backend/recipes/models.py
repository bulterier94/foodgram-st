from django.db import models
from django.core.validators import MinValueValidator

from users.models import User
from ingredients.models import Ingredient


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        related_name='recipe_author',
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    name = models.CharField(
        unique=False,
        max_length=256,
        blank=False,
        null=False,
        verbose_name='Название',
    )
    text = models.TextField(
        blank=False,
        null=False,
        verbose_name='Комментарий',
    )
    cooking_time = models.IntegerField(
        blank=False,
        null=False,
        validators=[MinValueValidator(1)],
        verbose_name='Время приготовления',
    )
    image = models.ImageField(
        upload_to='recipe_images/',
        blank=False,
        null=False,
        verbose_name='Изображение',
    )

    class Meta:
        ordering = ['id',]
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientInRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        related_name='ingredient_in_recipe',
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='recipe_from_ingredient',
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )
    amount = models.IntegerField(
        blank=False,
        null=False,
        validators=[MinValueValidator(1)],
        verbose_name='Количество',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='ingredient_in_recipe'
            )
        ]

        verbose_name = 'ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'

    def __str__(self):
        ingredient = self.ingredient.name
        recipe = self.recipe.name
        return f'Ингредиент "{ingredient}" в рецепте "{recipe}"'
