from rest_framework import permissions

ACCESS_LEVEL = {
    'admin': 0,
    'moderator': 1,
    'user': 2,
}


def has_access(user, role):
    """Проверяет уровень доступа пользователя."""
    return (ACCESS_LEVEL[user.role] <= ACCESS_LEVEL[role]
            or user.is_staff)


class IsAdminPermission(permissions.BasePermission):
    """Разрешает действия с объектом только админу или суперпользователю."""
    def has_object_permission(self, request, view, obj):
        return has_access(request.user, 'admin')


class IsAdminOrReadOnlyPermission(permissions.BasePermission):
    """
    Разрешает получить объект любому пользователю,
    изменение или удаление объекта доступно только админу.
    """
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or has_access(request.user, 'admin'))


class IsAuthorOrReadOnlyPermission(permissions.BasePermission):
    """
    Разрешает получить объект любому пользователю,
    изменение или удаление объекта доступно автору,
    модератору и админу.
    """
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user == obj.author  # Обязательно проверить что поле в модели называется author
                or has_access(request.user, 'moderator'))
