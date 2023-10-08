"""Настройки конфигурации приложения Users."""

from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Класс, конфигурирующий приложение Users."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
