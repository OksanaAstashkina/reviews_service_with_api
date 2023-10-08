"""Модель CustomUser в интерфейсе администратора."""

from django.contrib import admin

from users.models import CustomUser


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    """Отображение данных модели CustomUser в интерфейсе администратора."""

    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'bio',
        'role',
        'confirmation_code'
    )
    search_fields = ('username', 'role')
    list_filter = ('username', 'role')
    empty_value_display = '-пусто-'
