from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import exceptions, serializers, status
from rest_framework.validators import UniqueValidator

User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ('email', 'username',)

    def validate_username(self, value):
        if value == 'me':
            raise exceptions.ValidationError(
                'Имя пользователя не может быть: me')
        return value


class TokenSerializator(serializers.ModelSerializer):
    username = serializers.CharField()
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
