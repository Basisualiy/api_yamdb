from django.contrib.auth import get_user_model
from rest_framework import exceptions, serializers

User = get_user_model()


class UsersSerializer(serializers.ModelSerializer):
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
