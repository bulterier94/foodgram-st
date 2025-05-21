from django.apps import AppConfig


class FavoriteRecipesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'favorite_recipes'

    verbose_name = 'Рецепты в избранном'
