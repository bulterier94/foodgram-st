from django.contrib import admin

from .models import Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'subscriber',
        'subscribed_on',
    )
    search_fields = ('subscriber__username',)

    search_help_text = 'Поиск по подписчику.'
