"""Представления для приложения API."""

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (CreateModelMixin,
                                   DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (AllowAny,
                                        IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken

from api.filters import TitleFilter
from api.permissions import (AdminOnlyPermission,
                             AdminOrReadOnlyPermission,
                             AuthorAdminModeratorOrReadOnlyPermission)
from api.serializers import (CategorySerializer,
                             CommentSerializer,
                             GenreSerializer,
                             ReviewSerializer,
                             SignUpSerializer,
                             TitleListRetrieveSerializer,
                             TitleSerializer,
                             TokenSerializer,
                             UserMeEditSerializer,
                             UserSerializer)
from reviews.models import Category, Genre, Review, Title
from users.models import CustomUser


class UsersViewSet(ModelViewSet):
    """Представление для создания и редактирования пользователей."""

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, AdminOnlyPermission)
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    http_method_names = ('get', 'post', 'patch', 'delete')

    @action(methods=['GET', 'PATCH'],
            detail=False,
            permission_classes=(IsAuthenticated,),
            serializer_class=UserMeEditSerializer,
            url_path='me')
    def get_current_user_info(self, request):
        """Получение и частичное редактирование информации о себе."""
        serializer = self.get_serializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class APISignup(APIView):
    """Представление для регистрации пользователей."""

    permission_classes = (AllowAny,)

    @staticmethod
    def send_email(data):
        """Отправка письма по e-mail."""
        try:
            email = EmailMessage(
                subject=data['email_subject'],
                body=data['email_body'],
                to=[data['to_email']]
            )
            email.send()
        except Exception as error:
            return Response({'error': str(error)},
                            status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        """Регистрация пользователя и отправка кода подтверждения по e-mail."""
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        confirmation_code = default_token_generator.make_token(user)
        email_body = (
            f'Рады видеть Вас, {user.username}.'
            f'Код подтверждения для доступа: {confirmation_code}'
        )
        data = {
            'email_body': email_body,
            'to_email': user.email,
            'email_subject': 'Код подтверждения для доступа к ресурсу!'
        }
        self.send_email(data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class APIGetToken(APIView):
    """Представление для получения токена."""

    def post(self, request):
        """Получение токена."""
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            user = CustomUser.objects.get(username=data['username'])
        except CustomUser.DoesNotExist:
            return Response(
                {'username': 'Нет такого пользователя.'},
                status=status.HTTP_404_NOT_FOUND
            )
        if data.get('confirmation_code') == user.confirmation_code:
            token = AccessToken.for_user(user)
            return Response({'token': str(token)},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class TitleViewSet(ModelViewSet):
    """Представление для произведений."""

    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    serializer_class = TitleSerializer
    permission_classes = (AdminOrReadOnlyPermission,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = TitleFilter
    search_fields = ('name',)

    def get_serializer_class(self):
        """Выбор сериализатора данных в зависимости от метода запроса."""
        if self.request.method == 'GET':
            return TitleListRetrieveSerializer
        return TitleSerializer


class CategoryGenreViewSet(ListModelMixin,
                           CreateModelMixin,
                           DestroyModelMixin,
                           GenericViewSet):
    """Родительский класс для категорий и жанров."""

    permission_classes = (AdminOrReadOnlyPermission,)
    lookup_field = 'slug'
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class CategoryViewSet(CategoryGenreViewSet):
    """Представление для категорий произведений."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CategoryGenreViewSet):
    """Представление для жанров произведений."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ReviewViewSet(ModelViewSet):
    """Представление для отзывов на произведения."""

    serializer_class = ReviewSerializer
    permission_classes = (AuthorAdminModeratorOrReadOnlyPermission,
                          IsAuthenticatedOrReadOnly)
    pagination_class = LimitOffsetPagination

    def _get_title(self):
        """Получение произведения для отзыва."""
        return get_object_or_404(Title, id=self.kwargs['title_id'])

    def get_queryset(self):
        """Получение списка отзывов на выбранное произведение."""
        title = self._get_title()
        return title.reviews.all()

    def perform_create(self, serializer):
        """Создание отзыва на выбранное произведение."""
        title = self._get_title()
        user = self.request.user
        serializer.save(author=user, title=title)


class CommentViewSet(ModelViewSet):
    """Представление для комментариев к отзывам."""

    serializer_class = CommentSerializer
    permission_classes = (AuthorAdminModeratorOrReadOnlyPermission,
                          IsAuthenticatedOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def _get_review(self):
        """Получение отзыва для комментариев."""
        return get_object_or_404(Review, id=self.kwargs['review_id'])

    def get_queryset(self):
        """Получение списка комментариев на выбранный отзыв."""
        review = self._get_review()
        return review.comments.all()

    def perform_create(self, serializer):
        """Создание комментария на выбранный отзыв."""
        review = self._get_review()
        user = self.request.user
        serializer.save(author=user, review=review)
