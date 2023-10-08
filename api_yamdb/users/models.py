"""Описание моделей приложения Users."""

from django.contrib.auth.models import AbstractUser
from django.db import models

from users.validators import validate_username


class CustomUser(AbstractUser):
    """Модель для пользователей."""

    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLE_CHOICES = [
        (ADMIN, 'admin'),
        (MODERATOR, 'moderator'),
        (USER, 'user')
    ]
    username = models.CharField(
        'Пользовательское имя',
        max_length=150,
        unique=True,
        validators=[validate_username]
    )
    email = models.EmailField(
        'Email',
        max_length=254,
        unique=True
    )
    bio = models.TextField(
        'Биография',
        null=True,
        blank=True
    )
    role = models.CharField(
        'Пользовательская роль',
        max_length=9,
        choices=ROLE_CHOICES,
        default=USER
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=254,
        null=True,
        blank=False,
        default='None')

    class Meta:
        """Определение порядка объек-в CustomUser по умолч-ю и имени модели."""

        ordering = ('username', )
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        """Строковое представление объекта CustomUser по username."""
        return self.username

    @property
    def is_admin(self):
        """Определение роли администратора."""
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        """Определение роли модератора."""
        return self.role == self.MODERATOR

    @property
    def is_user(self):
        """Определение роли пользователя."""
        return self.role == self.USER
