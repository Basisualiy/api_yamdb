from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import exceptions, serializers, status
from rest_framework.validators import UniqueValidator

User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя."""
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        max_length=254)

    class Meta:
        model = User
        fields = ('email', 'username',)

    def validate_email(self, value):
        if len(value) > 254:
            raise exceptions.ValidationError(
                'Email не может больше 254 символов')
        return value

    def validate_username(self, value):
        if value == 'me':
            raise exceptions.ValidationError(
                'Имя пользователя не может быть: me')
        if len(value) > 150:
            raise exceptions.ValidationError(
                'Имя пользователя не может быть больше 150 символов')
        return value


class TokenSerializator(serializers.ModelSerializer):
    """Сериализатор для авторизации пользователя и выдачи ему токена."""
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(source='password')

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')

    def validate(self, data):
        try:
            username = data['username']
            confirmation_code = data['password']
        except KeyError:
            raise exceptions.ValidationError(code=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(User, username=username)
        if not user.check_password(confirmation_code):
            raise exceptions.ValidationError('Неверный код подтверждения.',
                                             code=status.HTTP_400_BAD_REQUEST)
        return data
