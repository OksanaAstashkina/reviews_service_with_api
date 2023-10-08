"""Кастомные фильтры для приложения API."""

from django_filters import CharFilter, FilterSet

from reviews.models import Title


class TitleFilter(FilterSet):
    """Фильтрация произведений."""

    category = CharFilter(field_name='category__slug')
    genre = CharFilter(field_name='genre__slug')

    class Meta:
        """Поля фильтрации произведений."""

        fields = ('name', 'category', 'genre', 'year')
        model = Title
