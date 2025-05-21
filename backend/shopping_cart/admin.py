from django.contrib import admin

from .models import ShoppingCart


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe',
    )
    search_fields = (
        'user__email',
    )
    search_help_text = 'Поиск по электронной почте пользователя.'
