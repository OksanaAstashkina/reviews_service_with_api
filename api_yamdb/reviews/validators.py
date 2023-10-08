"""Валидаторы для приложения Reviews."""

import datetime

from django.core.validators import MaxValueValidator


def max_value_current_year(value):
    """Валидация value на отсутствие превышения значения текущего года."""
    current_year = datetime.date.today().year
    return MaxValueValidator(current_year)(value)
