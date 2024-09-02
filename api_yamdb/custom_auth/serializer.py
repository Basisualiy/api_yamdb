from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import exceptions, serializers

User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username',)

    def validate_username(self, value):
        if value == 'me':
            raise exceptions.ValidationError(
                'Имя пользователя не может быть: me')
        return value


class TokenSerializator(serializers.ModelSerializer):
    confirmation_code = serializers.CharField(source='password')

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')

    # def validate_username(self, value):
    #     try:
    #         User.objects.get(username=value)
    #     except ObjectDoesNotExist:
    #         raise exceptions.ValidationError('Пользователь не найден.')
    #     return value

    def validate_confirmation_code(self, value):
        try:
            user = User.objects.get(username=self.initial_data.get('username'))
        except ObjectDoesNotExist:
            raise exceptions.ValidationError('Пользователь не найден.')
        if not user.check_password(value):
            raise exceptions.ValidationError()
        return value
