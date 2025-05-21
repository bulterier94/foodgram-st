from django.contrib import admin
from django.db.models import Count

from .models import Recipe, IngredientInRecipe


class IngredientInRecipeInline(admin.TabularInline):
    model = IngredientInRecipe
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientInRecipeInline,)
    list_display = (
        'name',
        'author',
        'favorites_count',
    )
    search_fields = (
        'name',
        'author__username',
    )
    search_help_text = 'Поиск по названию рецепта и нику автору.'
    readonly_fields = ('favorites_count',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(
            _favorites_count=Count('favorite_recipe', distinct=True)
        )

    def favorites_count(self, obj):
        return obj._favorites_count
    favorites_count.short_description = 'В избранном у пользователей'


@admin.register(IngredientInRecipe)
class IngredientInRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'recipe',
        'ingredient',
        'amount',
        'get_measurement_unit',
    )
    search_fields = (
        'ingredient__name',
    )

    search_help_text = 'Поиск по названию ингредиента.'

    def get_measurement_unit(self, obj):
        return obj.ingredient.measurement_unit
    get_measurement_unit.short_description = 'Единица измерения'
