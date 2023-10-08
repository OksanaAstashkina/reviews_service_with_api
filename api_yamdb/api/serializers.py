"""Сериализаторы для приложения API."""

from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db.utils import IntegrityError
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import (CharField,
                                        EmailField,
                                        IntegerField,
                                        ModelSerializer)
from rest_framework.validators import ValidationError

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import CustomUser
from users.validators import validate_username


class UserSerializer(ModelSerializer):
    """Сериализатор создания и редактирования пользователей."""

    class Meta:
        """Определение полей сериализатора пользователей."""

        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        model = CustomUser


class UserMeEditSerializer(UserSerializer):
    """Сериализатор создания и редактирования пользователей для <me>."""

    role = CharField(read_only=True)


class SignUpSerializer(ModelSerializer):
    """Сериализатор регистрации пользователей."""

    username = CharField(
        validators=[
            UnicodeUsernameValidator(),
            validate_username
        ],
        max_length=150,
    )
    email = EmailField(max_length=254)

    class Meta:
        """Определение полей сериализатора регистрации пользователей."""

        fields = (
            'username',
            'email'
        )
        model = CustomUser

    def create(self, validated_data):
        """Создание/получение пользователя."""
        try:
            user, _ = CustomUser.objects.get_or_create(**validated_data)
        except IntegrityError as e:
            if 'username' in str(e):
                raise ValidationError(
                    'Пользователь с таким именем уже существует.'
                    'Пожалуйста, выберите другое имя пользователя.'
                )
            elif 'email' in str(e):
                raise ValidationError(
                    'Пользователь с такой почтой уже существует.'
                    'Пожалуйста, используйте другой адрес электронной почты.'
                )
            else:
                raise ValidationError(
                    'Произошла ошибка при создании пользователя.'
                    'Пожалуйста, проверьте введенные данные и попробуйте снова'
                )
        return user


class TokenSerializer(ModelSerializer):
    """Сериализатор получения токена."""

    username = CharField(required=True)
    confirmation_code = CharField(required=True)

    class Meta:
        """Определение полей сериализатора получения токена."""

        fields = (
            'username',
            'confirmation_code'
        )
        model = CustomUser


class CategorySerializer(ModelSerializer):
    """Сериализатор категорий произведений."""

    class Meta:
        """Поля сериализатора категорий произведений."""

        fields = (
            'name',
            'slug'
        )
        model = Category


class GenreSerializer(ModelSerializer):
    """Сериализатор жанров произведений."""

    class Meta:
        """Поля сериализатора жанров произведений."""

        fields = (
            'name',
            'slug'
        )
        model = Genre


class TitleListRetrieveSerializer(ModelSerializer):
    """Сериализатор произведений для режима чтения."""

    category = CategorySerializer(read_only=True,)
    genre = GenreSerializer(
        read_only=True,
        many=True
    )
    rating = IntegerField(read_only=True,)

    class Meta:
        """Поля сериализатора произведений для режима чтения."""

        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )
        model = Title


class TitleSerializer(ModelSerializer):
    """Сериализатор произведений для режима записи и редактирования."""

    category = SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(), many=True
    )
    rating = IntegerField(read_only=True,)

    class Meta:
        """Поля сериализатора произведений для режима записи/редактирования."""

        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )
        model = Title


class ReviewSerializer(ModelSerializer):
    """Сериализатор отзывов на произведения."""

    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        """Поля сериализатора отзывов на произведения."""

        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date'
        )
        model = Review

    def validate(self, data):
        """Пользователь может оставить только один отзыв на произведение."""
        title = self.context['view'].kwargs.get('title_id')
        user = self.context['request'].user
        if not self.instance and Review.objects.filter(title=title,
                                                       author=user).exists():
            raise ValidationError(
                'Пользователь может оставить только один отзыв на произведение'
            )
        return data


class CommentSerializer(ModelSerializer):
    """Сериализатор комментариев к отзывам."""

    author = SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        """Поля сериализатора комментариев к отзывам."""

        fields = (
            'id',
            'text',
            'author',
            'pub_date'
        )
        model = Comment
