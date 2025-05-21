from django.contrib import admin

from .models import RecipeShortLink


@admin.register(RecipeShortLink)
class RecipeShortLinkAdmin(admin.ModelAdmin):
    list_display = (
        'recipe',
        'clicks',
    )
    search_fields = (
        'recipe__name',
    )

    search_help_text = 'Поиск по названию рецепта.'
