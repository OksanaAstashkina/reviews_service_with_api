"""Кастомные пермишены для приложения API."""

from rest_framework.permissions import BasePermission, SAFE_METHODS


class AdminOrReadOnlyPermission(BasePermission):
    """Разрешения на доступ к произведениям, категориям и жанрам.

    Чтение - все (без Токена).
    Полный доступ - только администратор или суперюзер Django.
    """

    def has_permission(self, request, view):
        """Разрешения на уровне запроса к произведениям,категориям и жанрам."""
        if request.method in SAFE_METHODS:
            return True
        return (request.user.is_authenticated
                and (request.user.is_admin or request.user.is_superuser))


class AdminOnlyPermission(BasePermission):
    """Разрешения на доступ к данным пользователей.

    Чтение и частич. редактирование своих данных - все пользователи.
    Полный доступ - администратор или суперюзер Django.
    """

    def has_permission(self, request, view):
        """Разрешения на уровне запроса к данным пользователей."""
        return (request.user.is_authenticated
                and (request.user.is_admin or request.user.is_superuser))


class AuthorAdminModeratorOrReadOnlyPermission(BasePermission):
    """Разрешения на доступ к отзывам и комментариям.

    Чтение - все (без Токена).
    Полный доступ к своим отзывам и комментариям - все пользователи.
    Редактирование и удаление любых отзывов и комментариев - модератор.
    Полный доступ - администратор или суперюзер Django.
    """

    def has_object_permission(self, request, view, obj):
        """Разрешения на уровне объекта к отзывам и комментариям."""
        if request.method in SAFE_METHODS:
            return True
        return (obj.author == request.user
                or request.user.is_moderator
                or request.user.is_admin)


# class RewiewValidatePermission(BasePermission):

#     def has_permission(self, request, view):
#         if request.method != 'POST':
#             return True
#         return False
