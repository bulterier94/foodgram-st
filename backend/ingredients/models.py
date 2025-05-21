from django.db import models


class Ingredient(models.Model):

    name = models.CharField(
        max_length=128,
        unique=True,
        blank=False,
        null=False,
        verbose_name='Название',
    )
    measurement_unit = models.CharField(
        max_length=64,
        unique=False,
        blank=False,
        null=False,
        verbose_name='Единица измерения',
    )

    class Meta:
        ordering = ['id',]
        verbose_name = 'ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name
