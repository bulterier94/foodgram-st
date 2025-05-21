from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator


class User(AbstractUser):

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'first_name', 'last_name', 'username', 'password',
    ]

    username = models.CharField(
        unique=True,
        max_length=150,
        blank=False,
        null=False,
        validators=[UnicodeUsernameValidator()],
        verbose_name='Ник',
    )
    email = models.EmailField(
        unique=True,
        max_length=254,
        blank=False,
        null=False,
        verbose_name='Адрес электронной почты',

    )
    first_name = models.CharField(
        unique=False,
        max_length=150,
        blank=False,
        null=False,
        verbose_name='Имя',
    )
    last_name = models.CharField(
        unique=False,
        max_length=150,
        blank=False,
        null=False,
        verbose_name='Фамилия',
    )
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True,)

    class Meta:
        ordering = ['id',]
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
