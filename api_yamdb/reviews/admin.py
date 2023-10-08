"""Модели в интерфейсе администратора."""

from django.contrib import admin

from reviews.models import Category, Comment, Genre, Review, Title


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Отображение данных модели Category в интерфейсе администратора."""

    list_display = (
        'name',
        'slug',
    )
    search_fields = (
        'name',
        'slug'
    )
    list_filter = (
        'name',
        'slug'
    )
    empty_value_display = '-пусто-'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Отображение данных модели Genre в интерфейсе администратора."""

    list_display = (
        'name',
        'slug',
    )
    search_fields = (
        'name',
        'slug'
    )
    list_filter = (
        'name',
        'slug'
    )
    empty_value_display = '-пусто-'


class GenreInline(admin.TabularInline):
    """Отображение жанров в модели Title в интерфейсе администратора."""

    model = Title.genre.through


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Отображение данных модели Title в интерфейсе администратора."""

    list_display = (
        'name',
        'year',
        'description',
        'category',
    )
    search_fields = (
        'name',
        'year',
        'description',
        'genre__name',
        'category__name'
    )
    list_filter = (
        'year',
        'genre__name',
        'category__name'
    )
    empty_value_display = '-пусто-'
    inlines = [GenreInline]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Отображение данных модели Review в интерфейсе администратора."""

    list_display = (
        'title',
        'text',
        'author',
        'score',
        'pub_date',
    )
    search_fields = (
        'title__name',
        'text',
        'author',
        'score',
        'pub_date'
    )
    list_filter = (
        'title__name',
        'author',
        'score',
        'pub_date'
    )
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Отображение данных модели Comment в интерфейсе администратора."""

    list_display = (
        'review',
        'text',
        'author',
        'pub_date',
    )
    search_fields = (
        'review',
        'text',
        'author',
        'pub_date'
    )
    list_filter = (
        'review',
        'author',
        'pub_date'
    )
    empty_value_display = '-пусто-'
