import secrets
from django.db import models
from django.urls import reverse

from recipes.models import Recipe


def generate_short_code():
    return secrets.token_urlsafe(6)[:6]


class RecipeShortLink(models.Model):
    recipe = models.OneToOneField(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_short_link',
        verbose_name='Рецепт',
    )
    code = models.CharField(
        max_length=10,
        unique=True,
        default=generate_short_code(),
        verbose_name='Код ссылки',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Создана',
    )
    clicks = models.PositiveIntegerField(
        default=0,
        verbose_name='Переходы',
    )

    class Meta:
        verbose_name = 'короткая ссылка на рецепт'
        verbose_name_plural = 'Короткие ссылки на рецепт'

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generate_short_code()
        super().save(*args, **kwargs)

    def get_short_url(self, request):
        if not self.code:
            self.code = generate_short_code()
            self.save()

        path = f'/s/{self.code}/'
        return request.build_absolute_uri(path) if request else path

    def get_absolute_url(self, request):
        return reverse(
            'recipe-detail-update-delete', kwargs={'recipe_id': self.recipe.pk}
        )

    def __str__(self):
        return f'Короткая ссылка на рецепт "{self.recipe.name}"'
