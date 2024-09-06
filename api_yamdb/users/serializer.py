from django.contrib.auth import get_user_model
from rest_framework import exceptions, serializers
from rest_framework.validators import UniqueValidator

User = get_user_model()


class UsersSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с пользователем."""
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        required=True,
        max_length=254)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )

    def validate_role(self, value):
        user = self.root._context['request'].user
        if user.role != 'admin' and not user.is_superuser:
            raise exceptions.PermissionDenied(
                'У вас нет прав на изменение роли.')
        return value


class MeSerializer(serializers.ModelSerializer):
    """Сериализатор для работы пользователя со своими данными."""
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        required=True,
        max_length=254)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )

    def validate_role(self, value):
        user = self.instance
        if user.role != 'admin' and not user.is_superuser:
            raise exceptions.PermissionDenied(
                'У вас нет прав на изменение роли.')
        return value
