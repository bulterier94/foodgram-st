from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'email',
        'username',
        'first_name',
        'last_name',
        'is_staff',
    )
    search_fields = (
        'email',
        'username',
    )
    search_help_text = 'Поиск по нику и адресу электронной почты.'
    empty_value_display = 'Не задано'
