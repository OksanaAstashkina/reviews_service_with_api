"""Описание моделей приложения Reviews."""

from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from reviews.validators import max_value_current_year
from users.models import CustomUser


class Category(models.Model):
    """Модель для категорий произведений."""

    name = models.CharField(
        'Наименование категории',
        max_length=256,
        help_text='Введите наименование категории'
    )
    slug = models.SlugField(
        'Slug категории',
        max_length=50,
        unique=True,
        help_text='Введите slug категории'
    )

    class Meta:
        """Определение порядка объек-в Category по умолчанию и имени модели."""

        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        """Строковое представление объекта Category по name."""
        return self.name


class Genre(models.Model):
    """Модель для жанров произведений."""

    name = models.CharField(
        'Наименование жанра',
        max_length=256,
        help_text='Введите наименование жанра'
    )
    slug = models.SlugField(
        'Slug жанра',
        max_length=50,
        unique=True,
        help_text='Введите slug жанра'
    )

    class Meta:
        """Определение порядка объектов Genre по умолчанию и имени модели."""

        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        """Строковое представление объекта Genre по name."""
        return self.name


class Title(models.Model):
    """Модель для произведений."""

    name = models.CharField(
        "Название",
        max_length=256,
        help_text='Введите название произведения'
    )
    year = models.PositiveSmallIntegerField(
        'Год выпуска',
        validators=[max_value_current_year],
        help_text='Введдите год выпуска произведения'
    )
    description = models.TextField(
        'Описание',
        max_length=250,
        blank=True,
        null=True,
        help_text='Введдите описание произведения'
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        related_name='titles',
        verbose_name='Slug жанра',
        help_text='Введдите жанр произведения'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Slug категории',
        null=True,
        help_text='Введите категорию произведения'
    )

    class Meta:
        """Определение порядка объектов Title по умолчанию и имени модели."""

        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        """Строковое представление объекта Title по name."""
        return self.name


class GenreTitle(models.Model):
    """Cвязующая модель для произведений и жанров."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE
    )

    class Meta:
        """Опред-ние порядка объек-в Title/Genre по умолч-ю и имени модели."""

        ordering = ('id',)
        verbose_name = 'Произведение/Жанр'
        verbose_name_plural = 'Произведения/Жанры'

    def __str__(self):
        """Строк. представление объекта Title/Genre по связке title-genre."""
        return f'{self.title} - {self.genre}'


class Review(models.Model):
    """Модель для отзывов."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Идентификатор произведения'
    )
    text = models.TextField(
        'Отзыв на произведение',
        max_length=400,
        help_text='Введите отзыв на произведение'
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва'
    )
    score = models.IntegerField(
        'Оценка произведения',
        validators=[
            MinValueValidator(1, message='Оценка не может быть меньше 1'),
            MaxValueValidator(10, message='Оценка не может быть больше 10'),
        ],
        help_text='Введите оценку произведения от 1 до 10'
    )
    pub_date = models.DateTimeField(
        'Дата создания отзыва',
        auto_now_add=True
    )

    class Meta:
        """Определение порядка объектов Review по умолчанию и имени модели.

        Определение уникальности связки 'author_of_review' - 'title'.
        """

        ordering = ('-pub_date',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='only_one_review'
            )
        ]

    def __str__(self):
        """Строк. представление объекта Review по первым 30 символам текста."""
        return self.text[:settings.LENGH_OF_TEXT]


class Comment(models.Model):
    """Модель для коментариев."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Идентификатор отзыва',
    )
    text = models.TextField(
        'Комментарий к отзыву',
        max_length=400,
        help_text='Введите комментарий на отзыв'
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария'
    )
    pub_date = models.DateTimeField(
        'Дата создания комментария',
        auto_now_add=True
    )

    class Meta:
        """Определение порядка объектов Review по умолчанию и имени модели."""

        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        """Строк. представление объекта Comment по перв. 30 символам текста."""
        return self.text[:settings.LENGH_OF_TEXT]
