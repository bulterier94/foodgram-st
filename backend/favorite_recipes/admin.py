from django.contrib import admin

from .models import FavoriteRecipe


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe',
    )
    search_fields = (
        'user__name',
    )

    search_help_text = 'Поиск по имени пользователя.'
