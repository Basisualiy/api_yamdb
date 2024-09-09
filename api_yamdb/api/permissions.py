from rest_framework import permissions

from reviews.models import ADMIN, MODERATOR


class IsAdminPermission(permissions.BasePermission):
    """Разрешает действия только админу или суперпользователю."""
    def has_permission(self, request, view):
        request.user.has_access = ADMIN
        return request.user.is_authenticated and request.user.has_access


class IsAdminOrReadOnlyPermission(permissions.BasePermission):
    """
    Разрешает получить объект любому пользователю,
    изменение или удаление объекта доступно только админу.
    """
    def has_permission(self, request, view):
        request.user.has_access = ADMIN
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user.has_access))


class IsAuthorOrReadOnlyPermission(permissions.BasePermission):
    """
    Разрешает получить объект любому пользователю,
    изменение или удаление объекта доступно автору,
    модератору и админу.
    """
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        request.user.has_access = MODERATOR
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                and (request.user == obj.author

                     or request.user.has_access))
